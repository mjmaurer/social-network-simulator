function isValidInput(n) {
    return parseFloat(n) >= 0 && parseFloat(n) <= 1 && n != "";
}

function runSimulation(frm) {
    diversity = frm.diversityP.value;
    uniqueness = frm.uniquenessP.value;
    reshare = frm.reshareP.value;
    if (isValidInput(diversity) && isValidInput(uniqueness) && isValidInput(reshare)) {
        simulating = true;
    } else {
        alert("Oops- make sure all fields are filled out! Accepted values are between 0.0 and 1.0.");
    }
}
