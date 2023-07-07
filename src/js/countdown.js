function countdown(due){
    const now = new Date();

    const rest = due.getTime() - now.getTime();
    const sec = Math.floor(rest / 1000) % 60;
    const min = Math.floor(rest / 1000 / 60) % 60;
    const hours = Math.floor(rest / 1000 / 60 / 60) % 24;
    const days = Math.floor(rest / 1000 / 60 / 60 / 24);
    const count = [days, hours, min, sec];

    return count;
}

function recalc(){
    const today = new Date();
    let nextSat = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 0, 0, 0, 0);
    nextSat.setDate(nextSat.getDate() + 6 - today.getDay());
    if (nextSat < today) {
        nextSat.setDate(nextSat.getDate() + 7);
    }
    const lefttime = countdown(nextSat);
    document.getElementById('left_days').textContent = lefttime[0];
    document.getElementById('left_hours').textContent = lefttime[1];
    document.getElementById('left_mins').textContent = String(lefttime[2]).padStart(2,'0');
    document.getElementById('left_secs').textContent = String(lefttime[3]).padStart(2,'0');
    refresh();
}

function refresh(){
    setTimeout(recalc, 1000);
}

recalc();
