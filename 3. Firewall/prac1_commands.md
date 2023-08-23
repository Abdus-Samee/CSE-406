# Installation
 - Download setup files and unzip them
   ```
   wget https://seedsecuritylabs.org/Labs_20.04/Files/Firewall/Labsetup.zip
   unzip Labsetup.zip
   ```

# Preparation of LKM
 - Module file <br />
   **hello.c**
   ```
    #include <linux/module.h>
    #include <linux/kernel.h>

    MODULE_LICENSE("GPL");
   
    int initialization(void){
     printk(KERN_INFO "Hello World!\n");
     return 0;
    }
   
    void cleanup(void){
     printk(KERN_INFO "Bye-bye World!.\n");
    }

    module_init(initialization);
    module_exit(cleanup);
   ```
 - **Makefile**
   ```
   obj-m += hello.o
   all:
     make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
   clean:
     make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
   ```
   The Makefile is run using the command: `$ make`

 - Running the Linux kernel module
   ```
   $ sudo insmod hello.ko (inserting a module)
   $ lsmod | grep hello (list modules)
   $ sudo rmmod hello (remove the module)
   $ dmesg (check the messages)
   ```
