[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y8WCUFW)

# Onshape Plugin for Cura
![Image](https://github.com/Gadgit83/CuraOnshapePlugin/assets/17674730/449c7351-a5ab-4307-8ae0-8ad89b2aa5f0)

This plugin allows you to access your Onshape parts and part studios directly from within Cura. This plugin is a very minimal 'proof of concept' for integrating Onshape into Cura. It currently allows you to navigate through your top level Folders and documents, and add parts to the print bed by double-clicking on them.

## Installation
To install the Onshape plugin, simply place the Onshape folder in the Cura plugins folder. The default location for this folder on Windows is C:\Users\[Username]\AppData\Roaming\cura\5.2\plugins. Your structure should then be plugins\Onshape\Onshape\onshape.py etc.

## Usage
To use the Onshape plugin, you'll need to provide your Onshape API token and secret. These can be entered in the settings.py file located in the Onshape plugin folder.

Once the plugin is installed and configured, you'll be able to access your Onshape parts and part studios from within Cura. To access the plugin, navigate to the 'Extensions' menu in Cura.
To navigate, double click each item - if it is a folder, or document then it will expand to show more documents or parts. 
If the item is a part, then it will be added to the print bed

## Limitations
- Very minimal 'proof of concept plugin', not fully featured, and could be significantly improved, but at least achieves basic functionality
- No Pagination on results, if you have more than 50 top level parts or folder in your 'My Onshape' then anything over 50 will not be shown - sorry
- Folders and documents are not differentiated - could really do with icons to show the difference
- All parts inside a document are listed, but not by part studio, so if you have same named parts, it will be difficult to spot the difference - really need to add part studio names or tree items to better identify parts
- Would really like to display Icons for Part studios and parts - shouldn't be too difficult
- The Plugin currently used 'unofficial' and undocumented API calls to Onshape, so it's possible they will stop or break these in the future. It's the ones to 'globaltreenodes', needed to get access to the folders at the root.

## Todo
- Pagination on results
- Differentiation between folders and documents
- Identifying parts by part studio
- Displaying icons for part studios and parts
- Once finished, tidy up and submit to the Cura Plugin store

## Support
If you have any issues or questions, please open an issue on this repository. I'm unlikely to be able to support any further or in short time, so worth having a go at forking and fixing yourself. Interestingly the bulk of this plugin was written with ChatGPT, and it would probably be quite helpful at adding features!

## Contribution
If you want to contribute to this plugin, please feel free to fork this repository and make pull requests with your contributions. I can at least help you test them out.
<<<<<<< HEAD

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y8WCUFW)
=======
>>>>>>> ed032b4ec712d4fe26305855c4a7c2dffdb267f3
