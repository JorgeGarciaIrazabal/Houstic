import {Page, NavController, NavParams} from 'ionic-angular';
import {HubsAPIService} from '../../services/HubsAPI';
import {ButtonsGuide} from '../buttons-guide/buttons-guide';

@Page({
    templateUrl: 'build/pages/getting-started/getting-started.html',
    providers: [HubsAPIService]
})
export class GettingStartedPage {

    static get parameters() {
        return [[NavController], [NavParams], [HubsAPIService]];
    }

    constructor(nav, navParams, _apiService) {
        this.api = _apiService.geApi();
        // the api is trying to reconnect every 1 second
        this.nav = nav;
    }

    goButtonsGuide() {
        this.nav.push(ButtonsGuide);
    }

    sendToAll(value) {
        this.api.HouseHub.server.setActuatorValue(0, 1, value)
            .then((response)=> console.log(JSON.stringify(response)),
                (message)=> console.error(JSON.stringify(message)))
            .finally(()=> console.log("Finally"));
    }
}
