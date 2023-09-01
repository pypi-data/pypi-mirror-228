# Fictus

Fictus generates a fake file system (FFS) that can be sent to stdout to display in documentation or presentations.


Example:

```Python
from fictus import DisplayModel, FictusFileSystem, Renderer

# Create a FictusFileSystem. The default root name of '/' has been replaced with 'c:'
ffs = FictusFileSystem("c:")

# Create some files in the current working directory.
ffs.mkfile("README.md", "LICENSE.md", ".ignore")

# Create dir and files relative to the current working directory.
ffs.mkdir("./files/docs")
ffs.cd("./files/docs")
ffs.mkfile("resume.txt", "recipe.wrd")

# Create/Change dir to music. Start with a `/` to ensure traversal from root.
ffs.mkdir("/files/music")
ffs.cd("/files/music")
ffs.mkfile("bing.mp3", "bang.mp3", "bop.wav")

# Generate a ffs structure to be printed to stdout as text.
ffs.cd("c:")  # jump to root; could have used "/" instead of "c:"
ffs.display()
```
Produces:
```
c:\
├─ files\
│  ├─ docs\
│  │  ├─ recipe.wrd
│  │  └─ resume.txt
│  └─ music\
│     ├─ bang.mp3
│     ├─ bing.mp3
│     └─ bop.wav
├─ .ignore
├─ LICENSE.md
└─ README.md
```

The tree displayed starts at current working directory. The same example
above with the current directory set to "c:/files/docs" produces:
```
c:\files\
   └─ docs\
      ├─ recipe.wrd
      └─ resume.txt
```
The way the Tree is displayed can be manipulated by creating a Display. A Display 
takes a Renderer and is injected into the Fictus File System. If a Display is not
provided, a default will be constructed and display the FFS as simple text.  

The display may need to be customized if you want the output to include HTML, 
Markdown, or other custom information.

Example:

```Python
# A customRenderer is created: adds an emoji before printing a File or Folder.
customRenderer = Renderer(
    "", "",  # Doc open/close
    "📄", "",  # File open/close
    "📁", "",  # Folder open/close
)

# Update display_model to the customRenderer
display_model = DisplayModel(customRenderer)
ffs.set_display_model(display_model)
ffs.display()
```
Produces:
```
c:\files\
   └─ 📁docs\
      ├─ 📄recipe.wrd
      └─ 📄resume.txt
```

## Install Using Pip
>pip install fictus

## Building/installing the Wheel locally:
To build the package requires setuptools and build.
>python3 -m build

Once built:
>pip install dist/fictus-*.whl --force-reinstall
