# DynDebug - Dynamic Debug

This library provides the ability to dynamically enable or disable debug through environment configuration.

## Usage

Use the factory method to create a debug instance.  You provide a `context` value which is used to enable/disable debug through configuration.
```
debug = Debug('MyContext1')
```

Use the debug instance to produce debug content
```
debug('This is some debug')    
```

Enable the debug at run time by setting the DEBUG environment property to the list of contexts for which you want debug enabled.
```
export DEBUG=MyContext1,MyContext2,...
```