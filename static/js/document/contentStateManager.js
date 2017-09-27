class ContentStateManager {

    constructor(field, maxSize = 100) {
        this.field = field;
        this.states = [];
        for (var i = 0; i < maxSize; i++) {
            this.states[i] = undefined;
        }
        this.states[0] = field.value;
        this.currentState = 0;
        this.lastState = 0;
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
        this.field.value = this.states[this.currentState];
    }


    newState(newState) {
        if (this.currentState != this.lastState) {
            for (var i = this.currentState + 1; i != this.lastState; i = (i+1) % this.states.length)
                this.states[i] = undefined;
        }
        this.currentState += 1;
        this.currentState %= this.states.length;;
        if (this.currentState < 0) this.currentState += this.states.length;
        this.lastState = this.currentState;
        this.states[this.currentState] = newState;
    }


    moveBackward() {
        if (!this.isOnFirstState()) {
            this.currentState -= 1;
            this.currentState %= this.states.length;
            if (this.currentState < 0) this.currentState += this.states.length;
            this.setState();
        }
    }


    moveForward() {
        if (!this.isOnLastState()) {
            this.currentState += 1;
            this.currentState %= this.states.length;
            if (this.currentState < 0) this.currentState += this.states.length;
            this.setState();
        }
    }

}