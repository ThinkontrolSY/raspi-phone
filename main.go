package main

import (
	"fmt"
	"log"
	"time"

	"github.com/warthog618/modem/at"
	"github.com/warthog618/modem/gsm"
	"github.com/warthog618/modem/serial"
)

func main() {
	// 配置串口
	port := "/dev/ttyAMA0"
	baudrate := 115200

	// 打开串口
	m, err := serial.New(serial.WithPort(port), serial.WithBaud(baudrate))
	if err != nil {
		log.Fatalf("Failed to open serial port: %v", err)
	}
	defer m.Close()

	// 创建 AT 指令集
	g := gsm.New(at.New(m, at.WithTimeout(time.Second)))
	if err = g.Init(); err != nil {
		log.Fatal(err)
	}

	g.AddIndication("+CLCC", func(info []string) {
		fmt.Println("Call information:")
		for _, line := range info {
			fmt.Println(line)
		}
	}, at.WithTrailingLine)

	for {
		time.Sleep(time.Second * 10) // 每秒钟执行一次
	}
}
