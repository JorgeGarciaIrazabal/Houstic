/**
 * Created by Jorge on 23/05/2016.
 */
angular.module('houstic.constants')
    .constant('components', {
        // Numbers have to match with enums.py
        0: {
            templateUrl: "templates/components/digitalIn.html",
            controller: "DigitalInCtrl"
        },
        1: {
            templateUrl: "templates/components/digitalOut.html",
            controller: "DigitalOutCtrl"
        },
        2: {
            templateUrl: "templates/components/analogIn.html",
            controller: "AnalogInCtrl"
        },
        3: {
            templateUrl: "templates/components/AnalogOut.html",
            controller: "AnalogOutCtrl"
        },
        4: {
            templateUrl: "templates/components/I2C.html",
            controller: "I2CCtrl"
        },
        5: {
            templateUrl: "templates/components/SPI.html",
            controller: "SPICtrl"
        }
    });