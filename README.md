> ⚠️ **Notice:**  
> This project has migrated to **[Codeberg](https://codeberg.org/Synchro/copr-libstrangle-git)**.  

Copr repository for git builds of libstrangle, commits are fetched every hour.

The packages in this repo should work on Fedora 39 and Fedora 40+.



## Installation 

Activate the repo with `sudo dnf copr enable jackgreiner/libstrangle-git` and then run `sudo dnf install libstrangle --refresh`.

To revert this, remove the package with `sudo dnf remove libstrangle` and then remove the copr repository with `sudo dnf copr remove jackgreiner/libstrangle-git`.


## Issues

Feel free to open issues when there are build issues I haven't fixed for a few days: https://github.com/ProjectSynchro/copr-libstrangle-git/issues

If you'd like me to attempt to package this for other RPM based distros like SUSE, open an issue and I'll see what I can do :)


## Building Locally Using fedpkg

To build this package locally using `fedpkg`, follow these steps:

1. **Clone the Repository**:
    ```sh
    fedpkg clone -a https://github.com/ProjectSynchro/copr-libstrangle-git.git
    cd copr-libstrangle-git
    ```

2. **Install Dependencies**:
    ```sh
    sudo dnf install fedpkg rpmdevtools
    sudo dnf install gcc gcc-c++ glibc-devel 
    ```
    - If you want to use this with 32bit x86 games also install
    ```sh
    sudo dnf install glibc-devel.i686 libgcc.i686 libstdc++-devel.i686
    ```

3. **Build the Package**:
    ```sh
    spectool -g libstrangle.spec
    fedpkg local
    ```
    - If you want to build a 32bit package:
    ```sh
    fedpkg local --arch i686
    ```

This will create the RPM packages under a folder named by whatever arch you are building for in the current directory.

For more information on using `fedpkg`, refer to the [Fedora Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/).
