/*
Copyright © 2020 NAME HERE <EMAIL ADDRESS>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
package cmd

import (
	"fmt"
  	"github.com/pkg/sftp"
  	"golang.org/x/crypto/ssh"
	"github.com/spf13/cobra"
	"os"
	"path"
	"time"
	"net"
	"bufio"
)

var (
	sftpserver string
	user string
	password string
	subdir	string
	err error
	sftpClient *sftp.Client
	remoteFileName string
	dstFile *sftp.File
	localFile *os.File
)

func getSftpClient(user, password, host string) (*sftp.Client, error) {
	var (
    	auth         []ssh.AuthMethod
    	addr         string
    	clientConfig *ssh.ClientConfig
    	sshClient    *ssh.Client
    	sftpClient   *sftp.Client
    	err          error
  	)

  	// 获取认证
	auth = make([]ssh.AuthMethod, 0)
	auth = append(auth, ssh.Password(password))
 
	clientConfig = &ssh.ClientConfig{
    	User:    user,
    	Auth:    auth,
    	Timeout: 30 * time.Second,
		HostKeyCallback: func(addr string, remote net.Addr, key ssh.PublicKey) error {
            return nil
    	},	  
	}
 
	// 链接SSH
	addr = fmt.Sprintf("%s:22", host)
 
  	if sshClient, err = ssh.Dial("tcp", addr, clientConfig); err != nil {
    	return nil, err
  	}
    

  	// create sftp 客户端
  	if sftpClient, err = sftp.NewClient(sshClient); err != nil {
    	return nil, err
 	}
 
 	return sftpClient, nil
	}


// getCmd represents the get command
var getCmd = &cobra.Command{
	Use:   "get",
	Short: "用于测试sftp账号get(读权限)",
	Long: `用于测试sftp账号是否具有读权限，使用账号密码登录sftp账号并下载空文件到本地. EP:
	./gosftp get -S [CA,FS,BC] -U XXX -D dir`,
	Run: func(cmd *cobra.Command, args []string) {
		sftpServerMap := make(map[string]string)

		sftpServerMap["CA"] = "sftpca.app.prd"
		sftpServerMap["FS"] = "sftpfs.app.prd"
		sftpServerMap["BC"] = "sftpbc.app.prd"

		input := bufio.NewScanner(os.Stdin)
		fmt.Printf("请输入SFTP密码:\n")
    	for input.Scan() {
        	line := input.Text()
        	password = line
        	break
  		}		

		if len(sftpserver) == 0 || len(user) == 0 || len(password) == 0 || len(subdir) == 0 {
			fmt.Printf("参数错误: sftp服务器, sftp用户名, sftp用户密码, 下载子目录均不能为空!\n")
			cmd.Help()
			return
		}

		if sftpServerMap[sftpserver] ==  "" {
			fmt.Printf("参数错误: sftp 服务器只能是BC, CA ,FS !\n")
			cmd.Help()
			return
		}
		sftpSvrIp := sftpServerMap[sftpserver]
		if sftpClient, err = getSftpClient(user, password, sftpSvrIp); err != nil {
			fmt.Println(err)
			fmt.Printf("登录失败, 请检查参数是否正确, 如参数均无误, 请联系SA\n")
			return
		}
		defer sftpClient.Close()

		var remoteFileName = fmt.Sprintf("%s/yqbstfplogin.test",subdir)
		localFileName := "yqbstfplogin.test"

		if dstFile, err = sftpClient.Open(remoteFileName); err != nil {
			fmt.Printf("下载失败: 目标sftp 上 %s 不存在测试文件, 请先执行./gosftp put 进行上传验证，如依然报错，请联系SA\n", subdir)
			return
		}
 		defer dstFile.Close()

		if localFile, err = os.Create(path.Join("/tmp/", localFileName)); err != nil {
			fmt.Printf("下载失败: 本地下载测试文件失败，请联系SA\n")
			return			
		}
		defer localFile.Close()		 

  		if _, err = dstFile.WriteTo(localFile); err != nil {
			  fmt.Printf("下载失败: 本地下载测试文件失败，请联系SA\n")
			  return
  		}
 
		fmt.Printf("测试文件下载成功，SFTP用户: %s 下子目录: %s 有读权限\n",user, subdir)
	},
}

func init() {
	rootCmd.AddCommand(getCmd)
	getCmd.Flags().StringVarP(&sftpserver, "sftpserver", "S", "", "sftp服务器")
	getCmd.Flags().StringVarP(&user, "user", "U", "", "sftp用户名")
	//getCmd.Flags().StringVarP(&password, "password", "P", "", "sftp密码")
	getCmd.Flags().StringVarP(&subdir, "subdir", "D", "", "下载的SFTP子目录")
}
