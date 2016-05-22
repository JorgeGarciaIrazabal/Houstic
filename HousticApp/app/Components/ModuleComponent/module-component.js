import {IONIC_DIRECTIVES} from 'ionic-angular';
import {NavController, NavParams} from 'ionic-angular';
import {Component, View, DynamicComponentLoader, ElementRef, Input} from 'angular2/core'

@Component({
    selector: 'module-component',
    template: '<ion-list><ion-item>I am an item</ion-item></ion-list>',
    directives: [IONIC_DIRECTIVES]
})
export class ModuleComponent {

    constructor() {
        debugger;
    }
}
