# Python Clean Architecture Example

A customer search system example based on the clean architecture.

## Usage

## Developing

You will need [poetry](https://python-poetry.org/) installed.

In project root run:

> make setup

To run the tests run:

> make test

## Architecture

The *clean architecture* approach was used in this project.

It contains two main submodules: **search** and **terminal**.

The **search** submodule contains the business rules that are essential for the application, that is, the domain entities and use cases.

The **terminal** submodule contains the presenter and the adapters, that is, the code in this layer interacts with the user and convert data from the format most convenient for the use cases and entities and then back from the use cases to the presenter.

![c4 component diagram](http://www.plantuml.com/plantuml/png/RL9DRzim3BtxLt0vfS1QNtRQRNFHeK0612jw3XY9ZON8eY5HDOnX_trKv0J9EbzeF7wynqTzSi7uR0bwaJ5zRTk8qyF1IP_tEL4q78I2F1WUsj5Za3pu-oJMkttRVRdV5kZrvwOTC0b5XNOT3oE7qZDgRTE84q_GvIGyK8GNmcXwU9crVcYQBSN4OLseFiFgLSDAu-gkQJfbHXSexhvp3XRZlCRHQV8owWVn8UBOEtCxTNK7lnlGxo9bRVofS_CCpxfFV4D3XQVppXpXAU904yTZWRQHtvsb1D8J55a99dK342QSGHXIfGeQA0cOHKrIpRUSBenPTE8tYwFKlRQpLR-SEN5pUASebSYY8Bn57YwqS6elX0NHMwWLAK7CNhMDM2JB_rZFUggRq64wRVgKWn77eVmlPfMv7xQe8X0CSxGke10aZkB20VRpgULS2iv-83yGw_ohkpow91XCqU5DzYWS_rLppYoMswKZgG5mT9xhdh0dcOW2oCHNujGATa6A3N-QvXVvvINLUwi19QFmRbEVmFacLvd7chdrxQhjWjVbbkHV)