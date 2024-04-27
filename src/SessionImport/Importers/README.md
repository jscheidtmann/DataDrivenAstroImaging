# Importers

Each implementation file here need to contain two classes:
 * One with the same name as the implementation file, i.e. if the file is named "XImporter.py", there needs to be a class definition for `XImporter`. 
   This class needs to be derived from `ImporterBase`
 * One with a suffix of "Meta", that means in "XImporter.py" there needs to be a class named `XImporterMeta`, that is derived from `ImporterMetaBase`.

 