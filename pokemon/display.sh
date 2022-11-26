pokemons=("bulbasaur" "charmander" "squirtle")
RANDOM=$$$(date +%s)

pokemon=${pokemons[$(($RANDOM % ${#pokemons[@]}))]}

echo
sh ~/pokemon/$pokemon.sh

