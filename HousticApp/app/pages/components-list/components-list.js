import {Page, NavController, NavParams} from 'ionic-angular';
import {HubsAPIService} from '../../services/HubsAPI';

@Page({
    templateUrl: 'build/pages/components-list/components-list.html'
})
export class ComponentListPage {
    static get parameters() {
        return [[NavController], [NavParams], [HubsAPIService]];
    }

    constructor(nav, navParams, _apiService) {
        var self = this;
        this.nav = nav;
        this.api = _apiService.getApi();
        // If we navigated to this page, we will have an item available as a nav param
        this.house = navParams.get('house');
        this.components = [];
        this.api.HouseHub.server.getAllComponents(this.house.id)
            .then((modules) => {
                for(var module in modules){
                    if(modules.hasOwnProperty(module)){
                        for(var componentKey in modules[module]){
                            if(modules[module].hasOwnProperty(componentKey)){
                                var component = modules[module][componentKey];
                                component.name = componentKey;
                                component.icon = 'bonfire';
                                self.components.push(component);
                            }
                        }
                    }
                }
            });

        this.icons = ['beaker', 'beer', 'bonfire'];

        this.items = [];
        for (let i = 0; i < 3; i++) {
            this.items.push({
                title: 'Componente ' + (i + 1),
                note: '',
                icon: this.icons[i]
            });
        }
    }
}
