# walkman 


A minimal random album selector for music libraries

## Installation


    git clone git@github.com:le-zouave/walkman.git
    pip install -r path/to/cloned/repo/walkman/requirements.txt

### Recommended configuration
Navigate to your home directory and open your `.bashrc` file with your favorite editor:

    cd
    vim .bashrc

Add the following lines anywhere, in this order:

    export WALKMAN_PATH=path/to/cloned/repo/walkman/
    alias walkman="python path/to/cloned/repo/walkman/walkman.py"

`walkman` can then be run from any directory.
## Usage


With the above configuration, `walkman` can be used as follows:

#### Random selection
    
    walkman -r

#### Random selection given artist

    walkman -a

You will then be prompted to enter an artist.

#### Random selection given a genre

    walkman -g

You will then be prompted to enter a genre.

#### Toggle vinyl collection for random selection

    walkman -r -v

A random selection will be made from the albums in the library which are also in a vinyl collection. This option is also compatible with the `-a` and `-g` options.

#### Specify a different library
The default music library is `libraries/lib_charles.txt`. If it exists in the `libraries` folder, a different library named `lib_individu.txt` can be specified for a random selection with

    walkman -l=individu -r
