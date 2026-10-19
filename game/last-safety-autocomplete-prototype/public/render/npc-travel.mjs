/** Staff first enter the building through the commons (presentation; engine places desks directly). */
export const STAFF_ENTRY_ROOM = 'commons';

export function entryRoomForMove(m, playerFromRoom) {
  if (!m || m.to == null) return null;
  if (m.from) return m.from;
  if (playerFromRoom) return playerFromRoom;
  return STAFF_ENTRY_ROOM;
}
