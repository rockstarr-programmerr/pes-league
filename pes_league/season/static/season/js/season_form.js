const teamsInput = document.getElementById('id_teams');
const turnsInput = document.getElementById('id_turns_count');
const roundsInput = document.getElementById('id_rounds_count');

teamsInput.addEventListener('input', updateRoundsCount);
turnsInput.addEventListener('input', updateRoundsCount);


function updateRoundsCount () {
  const roundsCount = getRoundsCount();
  roundsInput.value = roundsCount;
}

function getRoundsCount () {
  const teamsCount = getTeamsCount();
  const turnsCount = getTurnsCount();
  console.log(teamsCount, turnsCount)
  let roundsCount;

  if (isOdd(teamsCount)) {
    roundsCount = teamsCount * turnsCount;
  } else {
    roundsCount = (teamsCount - 1) * turnsCount;
  };

  return roundsCount;
}

function getTeamsCount () {
  let selectedCount = 0;
  for (const option of teamsInput.children) {
    if (option.selected) {
      selectedCount ++;
    };
  };
  return selectedCount;
}

function getTurnsCount () {
  let value = turnsInput.value;
  if (value !== '') {
    return parseInt(value);
  } else {
    return 0;
  }
}

function isOdd (number) {
  return number % 2 !== 0;
}
