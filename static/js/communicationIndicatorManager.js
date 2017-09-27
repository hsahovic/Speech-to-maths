class CommunicationIndicatorManager {
    constructor() {
        this.currentRequests = 0;
    }

    manageIndicator() {
        var div = document.getElementById("communication_indicator");
        if (this.currentRequests) div.style.display = 'inline-block';
        else div.style.display = 'none';
    }

    addRequest() {
        this.currentRequests++;
        this.manageIndicator();
    }

    endRequest() {
        this.currentRequests--;
        this.manageIndicator();
    }

}

var communicationIndicatorManager = new CommunicationIndicatorManager();