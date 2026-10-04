import sys

# Entry point
if __name__ == "__main__":

    # What OS is this script running on?
    if sys.platform == "win32":
        # Windows, run the Windows main function
        from windows import windows_main
        windows_main()
    elif sys.platform == "linux":
        # Linux, run the Linux main function
        from linux import linux_main
        linux_main()
    else:
        # This OS is not supported
        print("This operating system is not supported.")
        exit(1)