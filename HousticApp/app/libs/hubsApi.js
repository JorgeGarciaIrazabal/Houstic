'use strict';
/* jshint ignore:start */
/* ignore jslint start */
function HubsAPI(serverTimeout, wsClientClass, PromiseClass) {

    var messageID = 0,
        promisesHandler = {},
        defaultRespondTimeout = serverTimeout || 5000,
        thisApi = this,
        messagesBeforeOpen = [],
        emptyFunction = function () {},
        onOpenTriggers = [];

    PromiseClass = PromiseClass || Promise;
    if (!PromiseClass.prototype.finally) {
        PromiseClass.prototype.finally = function (callback) {
            var p = this.constructor;
            return this.then(
                function (value) {
                    return p.resolve(callback()).then(function () {
                        return value;
                    });
                },
                function (reason) {
                    return p.resolve(callback()).then(function () {
                        throw reason;
                    });
                });
        };
    }

    if (!PromiseClass.prototype.setTimeout) {
        PromiseClass.prototype.setTimeout = function (timeout) {
            clearTimeout(this._timeoutID);
            setTimeout(timeoutError(this._reject), timeout);
            return this;
        };
    }

    function timeoutError(reject) {
        return function () {
            reject(new Error('timeout error'));
        };
    }

    function toCamelCase(str) {
        return str.replace(/_([a-z])/g, function (g) { return g[1].toUpperCase(); });
    }

    this.clearTriggers = function () {
        messagesBeforeOpen = [];
        onOpenTriggers = [];
    };

    this.connect = function (url, reconnectTimeout) {
        return new PromiseClass(function (resolve, reject) {
            reconnectTimeout = reconnectTimeout || -1;
            function reconnect(error) {
                if (reconnectTimeout !== -1) {
                    window.setTimeout(function () {
                        thisApi.connect(url, reconnectTimeout);
                        thisApi.callbacks.onReconnecting(error);
                    }, reconnectTimeout * 1000);
                }
            }

            try {
                thisApi.wsClient = wsClientClass === undefined ? new WebSocket(url) : new wsClientClass(url);
            } catch (error) {
                reconnect(error);
                reject(error);
            }

            thisApi.wsClient.onopen = function () {
                resolve();
                thisApi.callbacks.onOpen(thisApi);
                onOpenTriggers.forEach(function (trigger) {
                    trigger();
                });
                messagesBeforeOpen.forEach(function (message) {
                    thisApi.wsClient.send(message);
                });
            };

            thisApi.wsClient.onclose = function (error) {
                reject(error);
                thisApi.callbacks.onClose(error);
                reconnect(error);
            };

            thisApi.wsClient.addOnOpenTrigger = function (trigger) {
                if (thisApi.wsClient.readyState === 0) {
                    onOpenTriggers.push(trigger);
                } else if (thisApi.wsClient.readyState === 1) {
                    trigger();
                } else {
                    throw new Error('web socket is closed');
                }
            };

            thisApi.wsClient.onmessage = function (ev) {
                try {
                    var promiseHandler,
                        msgObj = JSON.parse(ev.data);
                    if (msgObj.hasOwnProperty('reply')) {
                        promiseHandler = promisesHandler[msgObj.ID];
                        msgObj.success ? promiseHandler.resolve(msgObj.reply) : promiseHandler.reject(msgObj.reply);
                    } else {
                        msgObj.function = toCamelCase(msgObj.function);
                        var executor = thisApi[msgObj.hub].client[msgObj.function];
                        if (executor !== undefined) {
                            var replayMessage = {ID: msgObj.ID};
                            try {
                                replayMessage.reply = executor.apply(executor, msgObj.args);
                                replayMessage.success = true;
                            } catch (e) {
                                replayMessage.success = false;
                                replayMessage.reply = e.toString();
                            } finally {
                                if (replayMessage.reply instanceof PromiseClass) {
                                    replayMessage.reply.then(function (result) {
                                        replayMessage.success = true;
                                        replayMessage.reply = result;
                                        thisApi.wsClient.send(JSON.stringify(replayMessage));
                                    }, function (error) {
                                        replayMessage.success = false;
                                        replayMessage.reply = error;
                                        thisApi.wsClient.send(JSON.stringify(replayMessage));
                                    });
                                } else {
                                    replayMessage.reply = replayMessage.reply === undefined ? null : replayMessage.reply;
                                    thisApi.wsClient.send(JSON.stringify(replayMessage));
                                }
                            }
                        } else {
                            thisApi.callbacks.onClientFunctionNotFound(msgObj.hub, msgObj.function);
                        }
                    }
                } catch (err) {
                    thisApi.wsClient.onMessageError(err);
                }
            };

            thisApi.wsClient.onMessageError = function (error) {
                thisApi.callbacks.onMessageError(error);
            };
        });
    };

    this.callbacks = {
        onClose: emptyFunction,
        onOpen: emptyFunction,
        onReconnecting: emptyFunction,
        onMessageError: emptyFunction,
        onClientFunctionNotFound: emptyFunction
    };

    this.defaultErrorHandler = null;

    var constructMessage = function (hubName, functionName, args) {
        if (thisApi.wsClient === undefined) {
            throw new Error('ws not connected');
        }
        var promise,
            timeoutID = null,
            _reject;
        promise = new PromiseClass(function (resolve, reject) {
            args = Array.prototype.slice.call(args);
            var id = messageID++,
                body = {'hub': hubName, 'function': functionName, 'args': args, 'ID': id};
            promisesHandler[id] = {};
            promisesHandler[id].resolve = resolve;
            promisesHandler[id].reject = reject;
            timeoutID = setTimeout(timeoutError(reject), defaultRespondTimeout);
            _reject = reject;

            if (thisApi.wsClient.readyState === WebSocket.CONNECTING) {
                messagesBeforeOpen.push(JSON.stringify(body));
            } else if (thisApi.wsClient.readyState !== WebSocket.OPEN) {
                reject('webSocket not connected');
            } else {
                thisApi.wsClient.send(JSON.stringify(body));
            }
        });
        promise._timeoutID = timeoutID;
        promise._reject = _reject;
        return promise;
    };
    
    this.HouseHub = {};
    this.HouseHub.server = {
        __HUB_NAME : 'HouseHub',
        
        subscribeToHub : function (){
            
            return constructMessage('HouseHub', 'subscribe_to_hub', arguments);
        },

        listHouses : function (){
            
            return constructMessage('HouseHub', 'list_houses', arguments);
        },

        unsubscribeFromHub : function (){
            
            return constructMessage('HouseHub', 'unsubscribe_from_hub', arguments);
        },

        getAllComponents : function (houseId){
            
            return constructMessage('HouseHub', 'get_all_components', arguments);
        },

        getInstance : function (){
            
            return constructMessage('HouseHub', 'get_instance', arguments);
        },

        resetModule : function (houseId, moduleId){
            
            return constructMessage('HouseHub', 'reset_module', arguments);
        },

        getSubscribedClientsIds : function (){
            
            return constructMessage('HouseHub', 'get_subscribed_clients_ids', arguments);
        },

        componentWrite : function (houseId, moduleId, componentKey, value){
            
            return constructMessage('HouseHub', 'component_write', arguments);
        },

        stopModuleCommunication : function (houseId, moduleId){
            
            return constructMessage('HouseHub', 'stop_module_communication', arguments);
        },

        componentRead : function (houseId, moduleId, componentKey){
            
            return constructMessage('HouseHub', 'component_read', arguments);
        },

        create : function (){
            
            return constructMessage('HouseHub', 'create', arguments);
        }
    };
    this.HouseHub.client = {};
    this.UserHub = {};
    this.UserHub.server = {
        __HUB_NAME : 'UserHub',
        
        subscribeToHub : function (){
            
            return constructMessage('UserHub', 'subscribe_to_hub', arguments);
        },

        unsubscribeFromHub : function (){
            
            return constructMessage('UserHub', 'unsubscribe_from_hub', arguments);
        },

        login : function (userJson){
            
            return constructMessage('UserHub', 'login', arguments);
        },

        getSubscribedClientsIds : function (){
            
            return constructMessage('UserHub', 'get_subscribed_clients_ids', arguments);
        },

        getMyHouses : function (){
            
            return constructMessage('UserHub', 'get_my_houses', arguments);
        },

        removeHouse : function (houseId){
            
            return constructMessage('UserHub', 'remove_house', arguments);
        },

        register : function (userJson){
            
            return constructMessage('UserHub', 'register', arguments);
        },

        addHouse : function (house){
            
            return constructMessage('UserHub', 'add_house', arguments);
        }
    };
    this.UserHub.client = {};
    this.UtilsAPIHub = {};
    this.UtilsAPIHub.server = {
        __HUB_NAME : 'UtilsAPIHub',
        
        subscribeToHub : function (){
            
            return constructMessage('UtilsAPIHub', 'subscribe_to_hub', arguments);
        },

        getHubsStructure : function (){
            
            return constructMessage('UtilsAPIHub', 'get_hubs_structure', arguments);
        },

        getId : function (){
            
            return constructMessage('UtilsAPIHub', 'get_id', arguments);
        },

        getSubscribedClientsIds : function (){
            
            return constructMessage('UtilsAPIHub', 'get_subscribed_clients_ids', arguments);
        },

        setId : function (clientId){
            
            return constructMessage('UtilsAPIHub', 'set_id', arguments);
        },

        isClientConnected : function (clientId){
            
            return constructMessage('UtilsAPIHub', 'is_client_connected', arguments);
        },

        unsubscribeFromHub : function (){
            
            return constructMessage('UtilsAPIHub', 'unsubscribe_from_hub', arguments);
        }
    };
    this.UtilsAPIHub.client = {};
}
/* jshint ignore:end */
/* ignore jslint end */
    