/**
 * Created by Jorge on 28/03/2016.
 */
import {Injectable} from "angular2/core"

@Injectable()
export class HubsAPIService{

    constructor(){
        // todo: necessary to create an easy way to change between localhost and global server
        var MOBILE = 1; // defined in global server, HOUSE is 0
        this.api = new HubsAPI('ws://127.0.0.1:9517/' + MOBILE);
        this.api.connect(2);

        // todo: handle generic errors here
    }

    geApi(){
        return this.api;
    }
}