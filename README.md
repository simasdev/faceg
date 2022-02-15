# Faceg

Faceg is a simple tool that groups images by found faces.


## Usage

Provided directory will be searched for image files.

- Images that do not contain face will be copied to a new folder called 'FaceNotFound'
- Images with a face that was found in more than one photo will be copied to a new folder called 'People_[n]'
- Images with a face that was found only once will be copied to a new folder called 'Person_[n]'


Basic usage:
``` 
python main.py -d root\directory\goes\here
```

By default images will be copied to a new location, if you want them to be copied instead, pass this argument:
```
--move
```

By default only root folder will be searched, if you want all subdirectories to be searched as well, pass this argument:
```
--itr
```

