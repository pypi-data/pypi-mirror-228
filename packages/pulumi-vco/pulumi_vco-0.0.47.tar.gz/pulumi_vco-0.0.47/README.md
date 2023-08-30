[![NPM version](https://badge.fury.io/js/@fabianv-cloud%2Fvco.svg)](https://www.npmjs.com/package/@fabianv-cloud/vco)
[![PyPI version](https://badge.fury.io/py/pulumi-vco.svg)](https://badge.fury.io/py/pulumi-vco)
[![NuGet version](https://badge.fury.io/nu/Pulumi.Vco.svg)](https://badge.fury.io/nu/Pulumi.Vco)
# Pulumi Vco Native

A Pulumi provider for Whitesky.Cloud Virtual Cloud Operators.
<br><br>
The Whitesky.Cloud Vco Provider for Pulumi enables you to manipulate resources in your vco portal.
Please read the documentation or consult the API docs in your vco portal in order to properly understand how the resources work.

## Install plugin binary

Before using this package you need to install the resource-vco plugin. The latest release of which can be found [here](https://github.com/fabianv-cloud/pulumi-vco-native).
You then have to install the plugin on your system by storing the contents of the zipped file in: <br>
* Windows: %USERPROFILE%\.pulumi\plugins\resource-vco-{VERSION}
* Linux and MacOS: ~/.pulumi/plugins/resource-vco-{VERSION}
<br>

When you have moved the plugin to the appropriate directory you can install it using: 
```commandline
pulumi plugin install resource vco {VERSION}
```

## Install package
You can find links to the various packages at the top of the Readme. Once you have installed the desired package
you can import it into your program. Please consult the [examples](https://github.com/fabianv-cloud/pulumi-vco-native/tree/main/examples)
to figure out how to get started.
