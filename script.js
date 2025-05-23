const API_KEY = 'YOUR_API_KEY_HERE'; // Replace with your Football-Data.org API key

async function fetchMatches() {
    const today = new Date().toISOString().split('T')[0];
    const url = `https://api.football-data.org/v4/matches?competitions=PL&dateFrom=${today}&dateTo=${today}`;
    const resp = await fetch(url, {
        headers: { 'X-Auth-Token': API_KEY }
    });

    if (!resp.ok) {
        throw new Error('Failed to fetch match data');
    }

    const data = await resp.json();
    displayMatches(data.matches);
}

function displayMatches(matches) {
    const container = document.getElementById('matches');
    container.innerHTML = '';
    if (!matches || matches.length === 0) {
        container.textContent = 'No matches found.';
        return;
    }

    matches.forEach(match => {
        const card = document.createElement('div');
        card.className = 'match-card';

        const teams = document.createElement('div');
        teams.className = 'team';
        teams.appendChild(createTeam(match.homeTeam));
        teams.appendChild(createTeam(match.awayTeam));

        const score = document.createElement('div');
        score.className = 'score';
        if (match.score.fullTime.home !== null) {
            score.textContent = `${match.score.fullTime.home} - ${match.score.fullTime.away}`;
        } else {
            score.textContent = 'vs';
        }

        const status = document.createElement('div');
        status.className = 'status';
        const time = new Date(match.utcDate).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        status.textContent = `${match.status} \u2022 ${time}`;

        card.appendChild(teams);
        card.appendChild(score);
        card.appendChild(status);
        container.appendChild(card);
    });
}

function createTeam(team) {
    const wrapper = document.createElement('div');
    const img = document.createElement('img');
    img.src = team.crest;
    img.alt = team.name;
    const name = document.createElement('span');
    name.textContent = team.shortName || team.name;
    wrapper.appendChild(img);
    wrapper.appendChild(name);
    return wrapper;
}

fetchMatches().catch(err => {
    document.getElementById('matches').textContent = err.message;
});
