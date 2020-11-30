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
	"github.com/spf13/cobra"
	"os"
	"path"
	"bufio"
)
var putCmd = &cobra.Command{
	Use:   "put",
	Short: "用于测试sftp账号put(写权限)",
	Long: `用于测试sftp账号是否具有写权限，使用账号密码登录sftp账号并上传空文件到指定子目录. EP:
	./gosftp put -S [CA,FS,BC] -U XXX -D dir `,
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
			fmt.Printf("参数错误: sftp服务器, sftp用户名, sftp用户密码, 上传子目录均不能为空!\n")
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

		// 获取本地文件句柄
		localFileName := "yqbstfplogin.test"
		if localFile, err = os.Open(localFileName); err != nil {
			fmt.Printf("上传失败, 本地测试上传文件不存在, 请联系SA\n")
			return
		}
  		defer localFile.Close()

		// 获取本地文件句柄
  		if dstFile, err = sftpClient.Create(path.Join(subdir, localFileName)); err != nil {
			  fmt.Printf("上传失败，上传路径错误，请联系SA\n")
			  return
		}
  		defer dstFile.Close()
		
		// 上传
  		buf := make([]byte, 1024)
  		for {
    		n, _ := localFile.Read(buf)
    		if n == 0 {
      			break
    		}
    		dstFile.Write(buf)
  		}
		fmt.Printf("测试文件上传成功，SFTP用户: %s 下子目录: %s 有写权限\n",user, subdir)
	},
}

func init() {
	rootCmd.AddCommand(putCmd)
	putCmd.Flags().StringVarP(&sftpserver, "sftpserver", "S", "", "sftp服务器")
	putCmd.Flags().StringVarP(&user, "user", "U", "", "sftp用户名")
	putCmd.Flags().StringVarP(&password, "password", "P", "", "sftp密码")
	putCmd.Flags().StringVarP(&subdir, "subdir", "D", "", "上传的SFTP子目录")
}
