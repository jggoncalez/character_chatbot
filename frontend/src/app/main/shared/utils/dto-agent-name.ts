export const dtoAgentName = (agentName: string, characters: string[]): string => {
  const match = characters.find(character =>
    agentName.toLowerCase().includes(character.toLowerCase())
  );
  return match ?? agentName;
};