/**
 * Created by Jorge on 28/03/2016.
 */
import {Injectable} from "angular2/core"

@Injectable()
export class HubsAPIService{

    constructor(){
        console.log("creating hubsAPI");
        this.api = new HubsAPI();
        var MOBILE = 2; // defined in global server, HOUSE is 1
        this.api.connect('ws://127.0.0.1:9517/' + MOBILE, 2);
        // todo: necessary to create an easy way to change between localhost and global server

        // todo: handle generic errors here
    }

    getApi(){
        return this.api;
    }
}