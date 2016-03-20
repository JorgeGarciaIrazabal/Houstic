/* jshint ignore:start */
/* ignore jslint start */
function HubsAPI(url, serverTimeout) {
    'use strict';

    var messageID = 0,
        returnFunctions = {},
        defaultRespondTimeout = (serverTimeout || 5) * 1000,
        thisApi = this,
        messagesBeforeOpen = [],
        onOpenTriggers = [];
    url = url || '';

    this.clearTriggers = function () {
        messagesBeforeOpen = [];
        onOpenTriggers = [];
    };

    this.connect = function (reconnectTimeout) {
        reconnectTimeout = reconnectTimeout || -1;
        var openPromise = {
            onSuccess : function() {},
            onError : function(error) {}
        };
        function reconnect(error) {
            if (reconnectTimeout !== -1) {
                window.setTimeout(function () {
                    thisApi.connect(reconnectTimeout);
                    thisApi.callbacks.onReconnecting(error);
                }, reconnectTimeout * 1000);
            }
        }

        try {
            this.wsClient = new WebSocket(url);
        } catch (error) {
            reconnect(error);
            return;
        }

        this.wsClient.onopen = function () {
            openPromise.onSuccess();
            openPromise.onError = function () {};
            thisApi.callbacks.onOpen(thisApi);
            onOpenTriggers.forEach(function (trigger) {
                trigger();
            });
            messagesBeforeOpen.forEach(function (message) {
                thisApi.wsClient.send(message);
            });
        };

        this.wsClient.onclose = function (error) {
            openPromise.onError(error);
            thisApi.callbacks.onClose(error);
            reconnect(error);
        };

        this.wsClient.addOnOpenTrigger = function (trigger) {
            if (thisApi.wsClient.readyState === 0) {
                onOpenTriggers.push(trigger);
            } else if (thisApi.wsClient.readyState === 1) {
                trigger();
            } else {
                throw new Error("web socket is closed");
            }
        };

        this.wsClient.onmessage = function (ev) {
            try {
                var f,
                msgObj = JSON.parse(ev.data);
                if (msgObj.hasOwnProperty('replay')) {
                    f = returnFunctions[msgObj.ID];
                    if (msgObj.success && f !== undefined && f.onSuccess !== undefined) {
                        f.onSuccess(msgObj.replay);
                    }
                    if (!msgObj.success) {
                        if (f !== undefined && f.onError !== undefined) {
                            f.onError(msgObj.replay);
                        }
                    }
                } else {
                    f = thisApi[msgObj.hub].client[msgObj.function];
                    if (f!== undefined) {
                        var replayMessage = {ID: msgObj.ID}
                        try {
                            replayMessage.replay =  f.apply(f, msgObj.args);
                            replayMessage.success = true;
                        } catch(e){
                            replayMessage.success = false;
                            replayMessage.replay = e.toString();
                        } finally {
                            replayMessage.replay = replayMessage.replay === undefined ? null: replayMessage.replay;
                            thisApi.wsClient.send(JSON.stringify(replayMessage))
                        }
                    } else {
                        this.onClientFunctionNotFound(msgObj.hub, msgObj.function);
                    }
                }
            } catch (err) {
                this.onMessageError(err);
            }
        };

        this.wsClient.onMessageError = function (error) {
            thisApi.callbacks.onMessageError(error);
        };

        return { done: function (onSuccess, onError) {
                openPromise.onSuccess = onSuccess;
                openPromise.onError = onError;
            }
        };
    };

    this.callbacks = {
        onClose: function (error) {},
        onOpen: function () {},
        onReconnecting: function () {},
        onMessageError: function (error){},
        onClientFunctionNotFound: function (hub, func) {}
    };

    this.defaultErrorHandler = null;

    var constructMessage = function (hubName, functionName, args) {
        if(thisApi.wsClient === undefined) {
            throw Error('ws not connected');
        }
        args = Array.prototype.slice.call(args);
        var id = messageID++,
            body = {'hub': hubName, 'function': functionName, 'args': args, 'ID': id};
        if(thisApi.wsClient.readyState === WebSocket.CONNECTING) {
            messagesBeforeOpen.push(JSON.stringify(body));
        } else if (thisApi.wsClient.readyState !== WebSocket.OPEN) {
            window.setTimeout(function () {
                var f = returnFunctions[id];
                if (f !== undefined && f.onError !== undefined) {
                    f.onError('webSocket not connected');
                }
            }, 0);
            return {done: getReturnFunction(id, {hubName: hubName, functionName: functionName, args: args})};
        }
        else {
            thisApi.wsClient.send(JSON.stringify(body));
        }
        return getReturnFunction(id, {hubName: hubName, functionName: functionName, args: args});
    };

    var getReturnFunction = function (ID, callInfo) {

        function Future (ID, callInfo) {
            var self = this;
            this.done = function(onSuccess, onError, respondsTimeout) {
                if (returnFunctions[ID] === undefined) {
                    returnFunctions[ID] = {};
                }
                var f = returnFunctions[ID];
                f.onSuccess = function () {
                    try{
                        if(onSuccess !== undefined) {
                            onSuccess.apply(onSuccess, arguments);
                         }
                    } finally {
                        delete returnFunctions[ID];
                        self._finally();
                    }
                };
                f.onError = function () {
                    try{
                        if(onError !== undefined) {
                            onError.apply(onError, arguments);
                        } else if (thisApi.defaultErrorHandler !== null){
                            var argumentsArray = [callInfo].concat(arguments);
                            thisApi.defaultErrorHandler.apply(thisApi.defaultErrorHandler.apply, argumentsArray);
                        }
                    } finally {
                        delete returnFunctions[ID];
                        self._finally();
                    }
                };
                //check returnFunctions, memory leak
                respondsTimeout = undefined ? defaultRespondTimeout : respondsTimeout;
                if(respondsTimeout >=0) {
                    setTimeout(function () {
                        if (returnFunctions[ID] && returnFunctions[ID].onError) {
                            returnFunctions[ID].onError('timeOut Error');
                        }
                    }, defaultRespondTimeout);
                }
                return self;
            };
            this.finally = function (finallyCallback) {
                self._finally = finallyCallback;
            };
            this._finally = function () {};
        };
        return new Future(ID, callInfo)
    };

    
    this.UtilsAPIHub = {};
    this.UtilsAPIHub.server = {
        __HUB_NAME : 'UtilsAPIHub',
        
        getSubscribedClientsToHub : function (){
            
            return constructMessage('UtilsAPIHub', 'getSubscribedClientsToHub', arguments);
        },

        getId : function (){
            
            return constructMessage('UtilsAPIHub', 'getId', arguments);
        },

        isClientConnected : function (clientId){
            
            return constructMessage('UtilsAPIHub', 'isClientConnected', arguments);
        },

        unsubscribeFromHub : function (){
            
            return constructMessage('UtilsAPIHub', 'unsubscribeFromHub', arguments);
        },

        subscribeToHub : function (){
            
            return constructMessage('UtilsAPIHub', 'subscribeToHub', arguments);
        },

        setId : function (clientId){
            
            return constructMessage('UtilsAPIHub', 'setId', arguments);
        },

        getHubsStructure : function (){
            
            return constructMessage('UtilsAPIHub', 'getHubsStructure', arguments);
        }
    };
    this.UtilsAPIHub.client = {};
    this.HouseHub = {};
    this.HouseHub.server = {
        __HUB_NAME : 'HouseHub',
        
        setActuatorValue : function (componentId, value){
            
            return constructMessage('HouseHub', 'setActuatorValue', arguments);
        },

        getSensorValue : function (componentId){
            
            return constructMessage('HouseHub', 'getSensorValue', arguments);
        },

        getSubscribedClientsToHub : function (){
            
            return constructMessage('HouseHub', 'getSubscribedClientsToHub', arguments);
        },

        unsubscribeFromHub : function (){
            
            return constructMessage('HouseHub', 'unsubscribeFromHub', arguments);
        },

        getAllComponents : function (houseId){
            
            return constructMessage('HouseHub', 'getAllComponents', arguments);
        },

        subscribeToHub : function (){
            
            return constructMessage('HouseHub', 'subscribeToHub', arguments);
        }
    };
    this.HouseHub.client = {};
    this.UserHub = {};
    this.UserHub.server = {
        __HUB_NAME : 'UserHub',
        
        getMyHouses : function (){
            
            return constructMessage('UserHub', 'getMyHouses', arguments);
        },

        loggin : function (userJson){
            
            return constructMessage('UserHub', 'loggin', arguments);
        },

        getSubscribedClientsToHub : function (){
            
            return constructMessage('UserHub', 'getSubscribedClientsToHub', arguments);
        },

        unsubscribeFromHub : function (){
            
            return constructMessage('UserHub', 'unsubscribeFromHub', arguments);
        },

        removeHouse : function (houseId){
            
            return constructMessage('UserHub', 'removeHouse', arguments);
        },

        subscribeToHub : function (){
            
            return constructMessage('UserHub', 'subscribeToHub', arguments);
        },

        addHouse : function (house){
            
            return constructMessage('UserHub', 'addHouse', arguments);
        }
    };
    this.UserHub.client = {};
}
/* jshint ignore:end */
/* ignore jslint end */
    