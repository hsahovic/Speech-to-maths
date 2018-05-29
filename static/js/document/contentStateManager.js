class ContentStateManager {

    constructor(updateFunction, maxSize = 100, initialValue) {
        this.updateFunction = updateFunction;
        this.states = [];
        for (var i = 0; i < maxSize; i++) {
            this.states[i] = undefined;
        }
        this.states[0] = initialValue;
        this.currentState = 0;
        this.lastState = 0;
        this.manageQueueButtonsStyle();
    }


    isOnLastState() {
        return (this.currentState == this.lastState);
    }


    isOnFirstState() {
        var pos = (this.currentState - 1) % this.states.length;
        if (pos < 0) pos += this.states.length;
        return ((this.currentState == (this.lastState + 1) % this.states.length) || this.states[pos] == undefined);
    }


    setState() {
        this.updateFunction(this.states[this.currentState]);
    }


    newState(newState) {
        if (this.currentState != this.lastState) {
            for (var i = this.currentState + 1; i != this.lastState; i = (i + 1) % this.states.length)
                this.states[i] = undefined;
        }
        this.currentState += 1;
        this.currentState %= this.states.length;;
        if (this.currentState < 0) this.currentState += this.states.length;
        this.lastState = this.currentState;
        this.states[this.currentState] = newState;
        this.manageQueueButtonsStyle();
    }


    moveBackward() {
        this.setState();
        if (!this.isOnFirstState()) {
            this.currentState -= 1;
            this.currentState %= this.states.length;
            if (this.currentState < 0) this.currentState += this.states.length;
            this.setState();
        }
        this.manageQueueButtonsStyle();
    }


    moveForward() {
        if (!this.isOnLastState()) {
            this.currentState += 1;
            this.currentState %= this.states.length;
            if (this.currentState < 0) this.currentState += this.states.length;
            this.setState();
        }
        this.manageQueueButtonsStyle();
    }

    manageQueueButtonsStyle() {
        // Gestion de l'apparence des boutons en avant / en arrière
        if (this.isOnLastState()) {
            if (document.getElementById("moveForward").className.search(" disabled") == -1) {
                document.getElementById("moveForward").className += " disabled";
                document.getElementById("moveForward").disabled = true;
            }
        }
        else {
            document.getElementById("moveForward").className = document.getElementById("moveForward").className.replace(" disabled", "");
            document.getElementById("moveForward").disabled = false;
        }
        if (this.isOnFirstState()) {
            if (document.getElementById("moveBackward").className.search(" disabled") == -1) {
                document.getElementById("moveBackward").className += " disabled";
                document.getElementById("moveBackward").disabled = true;
            }
        }
        else {
            document.getElementById("moveBackward").className = document.getElementById("moveBackward").className.replace(" disabled", "");
            document.getElementById("moveBackward").disabled = false;
        }
    }

}