# Python program to program the neo and micro devices in different flashes.

from sys import argv
from subprocess import getoutput
from re import search
from os import system
import threading


class colors:
    END      = '\33[0m'
    BOLD     = '\33[1m'
    ITALIC   = '\33[3m'
    BLINK    = '\33[5m'

    WARNING = '\033[93m'
    ERROR = '\33[91m'
    DONE = '\33[92m'
    HEADER = '\033[94m'
    INFO = '\33[36m'

class Programming:
    device_list = []
    #micro_list = []
    wrong_count = 1

    def find_model(self):
        """Checks whether the storage medium is connected to the device or not."""
        try:
            # cmd defining here is just a workaround to stop pycharm warnings. You can remove this.
            cmd = None
            output_pattern = '/dev/disk'
            # Different types of flashes are defined to program the NEO thinux in them.
            if argv[1] == "neo":
                sandisk = f'/dev/disk/by-id/usb-SanDisk*'
                kingston = f'/dev/disk/by-id/usb-Kingston*'
                forza = f'/dev/disk/by-id/ata-NFS011*'
                kingspec = f'/dev/disk/by-id/ata-P4*'
                sata_SDV = f'/dev/disk/by-id/ata-SDV-16*'
                cmd = f'readlink -f {sandisk} {kingston} {forza} {kingspec} {sata_SDV}'
            # Checks the attached SD card if the programming option selected is MICRO thinux
            elif argv[1] == "micro":
                cmd = f'readlink -f /dev/disk/by-path/pci-0000:00:14.0-usb*'
            else:
                print(f'{colors.BOLD}{colors.ERROR}Error: Wrong argument passed!!!{colors.END}')
                exit(1)

            output_cmd = getoutput(cmd)
            output_cmd = output_cmd.split()
            output_length = len(output_cmd)
            print(output_cmd)
            if argv[1] == "micro":
                for index in range(output_length):
                    if len(output_cmd[index]) == 8:
                        self.device_list.append(output_cmd[index])
                    else:
                        dummy = output_cmd[index][-9:-1]
                        if dummy in self.device_list:
                            print(dummy)
                        else:
                            self.device_list.append(dummy)
            else:
                self.device_list = [output_cmd[index] for index in range(output_length) if len(output_cmd[index]) == 8]
            if not self.device_list:
                print(f'{colors.BOLD}{colors.ERROR}"No Storage media found!!!"{colors.END}')
            else:
                print(f'{colors.ITALIC}{colors.INFO}Storage media detected at labels {self.device_list} and number of storage devices are {len(self.device_list)} {colors.END}')
                self.umount_device()
                self.programming_choice()

        except Exception as e:
            print(f'{colors.ERROR}{colors.BOLD}{colors.BLINK}Find_model error: {colors.END}', e)
            exit(1)


    def umount_device(self):
        """ Umount the attached USB storage devices."""
        try:
            print(f'{colors.INFO}{colors.ITALIC}Unmounting the attached storage devices!!!!{colors.END}')
            for index in range(len(self.device_list)):
                umount_cmd = f'umount {self.device_list[index]}*>/dev/null 2>&1'
                system(umount_cmd)
            print(f'{colors.DONE}{colors.BOLD}{colors.BLINK}Devices are unmount!!!{colors.END}')
        except Exception as e:
            print(f'{colors.ERROR}{colors.BOLD}{colors.BLINK}Unmount_device error: {colors.END}', e)
            exit(1)

    def programming_choice(self):
        """Offers the choices like formatting the storage medium or program the medium to user."""
        try:
            choice = input(f'{colors.HEADER}{colors.BOLD}DO YOU WANT TO FORMAT THE STORAGE DEVICE OR DIRECTLY PROGRAM THINUX IN IT?{colors.INFO}(f/p/q): {colors.END}')
            if choice == "f":
                self.format_device()
                programming_choice = input(f'{colors.INFO}{colors.ITALIC}Do you want to program the storage devices or quit(p/q): {colors.END}')
                if programming_choice == "p":
                    self.image_choice()
                elif programming_choice == "q":
                    print(f'{colors.DONE}Quitting!!!{colors.END}')
                    exit(0)
                else:
                    print(f'{colors.ERROR}{colors.BLINK}No input provided, quitting!!!{colors.END}')
                    exit(1)
            elif choice == 'p':
                self.image_choice()
            elif choice == 'q':
                exit(0)
            else:
                print(f'{colors.WARNING}Wrong Choice entered!!!{colors.END}')
                while self.wrong_count != 3:
                    self.wrong_count += 1
                    self.programming_choice()
                print(f'{colors.ERROR}{colors.BOLD}{colors.BLINK}Too many wrong inputs, Quiting now!!!{colors.END}')
                exit(1)
        except Exception as e:
            print(f'{colors.ERROR}{colors.BOLD}{colors.BLINK}programming_choice error: {colors.END}', e)
            exit(1)

    def format_device(self):
        """Formats the storage medium."""
        try:
            print(f'{colors.INFO}{colors.ITALIC}Formatting the storage devices, please wait!!!{colors.END}')
            for index in range(len(self.device_list)):
                #format_cmd = f'mkfs.ext4 -F {self.device_list[index]} >/dev/null 2>&1'
                format_cmd = f'mkfs.ext4 -F {self.device_list[index]}'
                system(format_cmd)
            print(f'{colors.DONE}{colors.BOLD}{colors.BLINK}Formatting done!!!!{colors.END}')
        except Exception as e:
            print(f'{colors.ERROR}{colors.BOLD}{colors.BLINK}format_choice error: {colors.END}', e)
            exit(1)

    def image_choice(self):
        """ Selects whether to program the old image or new image in the NEO and Micro devices"""
        try:
            if argv[1] == "neo":
                image_choice = input(f'{colors.INFO}DO YOU WANT TO PROGRAM THE OLD OR NEW THINUX IN THE NEO DEVICE???(old/new): {colors.END}')
                if image_choice == "o" or image_choice == "old":
                    self.create_thread("old neo")
                elif image_choice == "n" or image_choice == "new":
                    self.create_thread("new neo")
                else:
                    print(f'{colors.ERROR}{colors.BLINK}{colors.BOLD}No input provided, quitting!!!{colors.END}')
            elif argv[1] == "micro":
                image_choice = input(f'{colors.INFO}DO YOU WANT TO PROGRAM THE OLD OR NEW THINUX IN THE MICRO DEVICE???(old/new/rep): {colors.END}')
                if image_choice == "o" or image_choice == "old":
                    self.create_thread("old micro")
                elif image_choice == "n" or image_choice == "new":
                    self.create_thread("new micro")
                elif image_choice == "r" or image_choice == "rep":
                    self.create_thread("rep micro")
                else:
                    print(f'{colors.ERROR}{colors.BLINK}No input provided, quitting!!!{colors.END}')

        except Exception as e:
            print(f'{colors.ERROR}{colors.BOLD}{colors.BLINK}image_choice error: {colors.END}', e)
            print("Image choice error: ", e)
            exit(1)

    def neo_program(self, thread, lock, image_choice):
        """Programs the storage medium."""
        try:
            mount_dir = "/mnt"
            if image_choice == "old neo":
                program_cmd4 = f'cd /storage/neo_micro/old_neo/ && bmaptool copy image.img {self.device_list[thread]} && sleep 2'
            else:
                program_cmd4 = f'cd /storage/neo_micro/new_neo/ && bmaptool copy image.img {self.device_list[thread]} && sleep 2'
            program_cmd5 = f'echo ",,L,-" | sfdisk --append {self.device_list[thread]} && sync && partprobe && \
                            umount {self.device_list[thread]}*'
            program_cmd6 = f'mkfs.ext4 -F {self.device_list[thread]}2 -L data && mount {self.device_list[thread]}1 \
                            {mount_dir}'
            program_cmd7 = f'grub-install --target=i386-pc --root-directory={mount_dir} --boot-directory={mount_dir}/boot \
                            --recheck {self.device_list[thread]} && umount {self.device_list[thread]}1'
            system(program_cmd4)
            lock.acquire()
            system(program_cmd5)
            system(program_cmd6)
            system(program_cmd7)
            lock.release()
        except Exception as e:
            print(f'{colors.ERROR}{colors.BOLD}{colors.BLINK}neo programming error: {colors.END}', e)
            exit(1)

    def micro_program(self, thread, lock, image_choice):
        """ Function to program Micro."""
        try:
            if image_choice == "old micro":
                micro_cmd1 = f'cd /storage/neo_micro/old_micro/ && bmaptool copy image.img {self.device_list[thread]} && sleep 2'
                micro_cmd2 = f'echo ",,L,-" | sfdisk --append {self.device_list[thread]}'
                micro_cmd3 = f'sync && partprobe && umount {self.device_list[thread]}'
                micro_cmd4 = f'mkfs.ext4 {self.device_list[thread]}2 -L data'
                system(micro_cmd1)
                lock.acquire()
                system(micro_cmd2)
                system(micro_cmd3)
                system(micro_cmd4)
                lock.release()
            elif image_choice == "new micro":
                micro_cmd1 = f'cd /storage/neo_micro/opipc-pc/ && bmaptool copy image.img {self.device_list[thread]} && sleep 1'
                system(micro_cmd1)
            else:
                micro_cmd1 = f'cd /storage/neo_micro/rep_micro/ && bmaptool copy image.img {self.device_list[thread]} && sleep 1'
                system(micro_cmd1)
        except Exception as e:
            print(f'{colors.ERROR}{colors.BOLD}{colors.BLINK}micro programming error: {colors.END}', e)
            exit(1)


    def create_thread(self, image_choice):
        """Generates thread according to the number of storage medium attached to the programming device."""
        try:
            threads = []
            lock = threading.Lock()
            for thread in range(len(self.device_list)):
                if argv[1] == "neo":
                    thread_instance = threading.Thread(target=self.neo_program, args=(thread, lock, image_choice))
                else:
                    thread_instance = threading.Thread(target=self.micro_program, args=(thread, lock, image_choice))
                threads.append(thread_instance)
                thread_instance.start()

            for created_thread in threads:
                print(created_thread)
                created_thread.join()
            exit_choice = input(f'{colors.INFO}{colors.ITALIC}Programming done!!!Do you want to continue or do you want to quit(c/q)? {colors.END}')
            if exit_choice == 'q':
                print(f'{colors.DONE}{colors.BOLD}{colors.BLINK}Quitting now!!!{colors.END}')
                exit(0)
            else:
                print(f'{colors.INFO}Restarting the program!!!!{colors.END}')
                self.find_model()
        except Exception as e:
            print(f'{colors.ERROR}{colors.BOLD}{colors.BLINK}create_thread error: {colors.END}', e)
            print("Create thread error: ", e)
            exit(1)


if __name__ == "__main__":
    program = Programming()
    program.find_model()

