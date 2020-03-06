#! /usr/bin/perl -w
#auther Barney by 20160508

use strict;
use DBI;
use Net::SSH::Perl;
use Mail::Sender;

sub main {
&db_init;
&db_update;
&info_print;
my $check_result=`cat data/result.txt | grep "Slave Server"`;
if($check_result) {
&mail_send;
}
else {
print "no behind!!\n";
}
}

sub ssh_get {
	my ($ip,$passwd,$socket)=@_;
	my $cmd="`which mysql`  -ubarney -ppasswd  -e 'show slave status\\G;' --socket=$socket | grep -i \"Seconds_Behind_Master\" |awk -F \":\" '{print \$2}'"; #有些mysql 是编译安装的。所以路径不一定对。。
	my $osuser="barney";
	my %params = (
		port => '22',
		protocal => '2,1',
	);
	my $ssh = Net::SSH::Perl->new($ip,%params);
	$ssh->login($osuser,$passwd,$socket);
	my ($out,$err,$exit) = $ssh->cmd($cmd);
	return ($out);
}


sub db_init {
	my $driver="DBI:mysql";
	my $database1="DB_OPS";
	my $user="barney";
	my $password='barney@123';
	my $db_connect = DBI->connect("$driver:$database1:mysql_socket=/var/run/mysqld/mysqld_new.sock","$user","$password");
}

sub db_update {
	my $db_connect=&db_init;
	my ($i,$j);
	$db_connect->do("SET NAMES utf8"); 
	my $db_status=$db_connect->prepare("select * from DB_OPS.t_master_db_instance;");
	$db_status->execute;
	
	my( $ip, $project, $behind ,$mysql_cmd,$socket,$check_flag );
	$db_status->bind_columns( undef, \$ip, \$project, \$behind, \$mysql_cmd, \$socket,\$check_flag);
	while( $db_status->fetch() ) {
		if ($ip =~ /192.168.1./ || $ip =~ /192.168.2./ || $ip =~ /192.168.3./ || $ip =~ /192.168.4./ || $ip =~ /192.168.5./ || $ip =~ /192.168.6./) {
			my $passwd="barney@1";
			my $i=&ssh_get($ip,$passwd,$socket);
			my $j=$i/3600;
			my $now_behind = sprintf("%.1f",$j);
			my $db_update = $db_connect->do("update DB_OPS.t_master_db_instance set db_behind='$now_behind' where db_ip='$ip';");
			if ($now_behind =~ /0./) {
				my $check_flag = $db_connect->do("update DB_OPS.t_master_db_instance set check_flag='0' where db_ip='$ip';");
			}
			else {
				my $check_flag = $db_connect->do("update DB_OPS.t_master_db_instance set check_flag='1' where db_ip='$ip';");
				}
		}

}
	$db_status->finish();
	$db_connect->disconnect();
}

sub info_print {
	my $data_dir="./data";
	mkdir $data_dir,0775;
	open(INFO,">$data_dir/result.txt");
	print INFO "Dear All:\n\n\n Slave info:\n\n ++++++++++++++++++++++++\n";
	&result_filter;
	print INFO "++++++++++++++++++++++++\n \n\n End Message from 192.168.2.104\n";
	close (INFO);
}

sub result_filter {	##将有延迟的数据筛选出来
	my $db_connect=&db_init;
	$db_connect->do("SET NAMES utf8");
	my $db_status=$db_connect->prepare("select db_ip,db_project,db_behind,socket from DB_OPS.t_master_db_instance where check_flag=1;");
	$db_status->execute;

	my( $ip, $project, $behind ,$socket);
	$db_status->bind_columns( undef, \$ip,\$project, \$behind, \$socket);
	while( $db_status->fetch() ) {
		my $behind_info="\t\tSlave Server: $ip Project Name: $project Behind Time: ${behind} hour Socket Time: $socket \n\n";
		print INFO "$behind_info";
	}
}


sub mail_send { 	##发送邮件通知
my $sender = new Mail::Sender
{
  		smtp    => 'mail.shidc.barney.com',
  		from    => 'ops@barney.com',
} or die "error";
	my $message = `cat ./data/result.txt`;
	if($sender-> MailMsg ({
             to      => 'ops@barney.com',
             subject => 'warnning!!! 从库落后',
             msg     =>  $message })<0)
{
  die "$Mail::Sender::Error/n";
}
$sender->Close();
}	


&main();