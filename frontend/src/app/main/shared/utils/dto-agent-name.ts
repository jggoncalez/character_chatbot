export const dtoAgentName = (agentName: string, characters: string[]): string => {
  if (!agentName || !characters?.length) return '';
  const match = characters.find(character =>
    agentName.toLowerCase().includes(character.toLowerCase())
  );
  return match ?? agentName;
};