using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace day16
{
    public class RoomNode
    {
        public Room Room {get;set;}
        public int Distance {get;set;}
        public bool visited {get;set;}
        public RoomNode(){}

        public RoomNode(Room room, int distance)
        {
            Room = room;
            Distance = distance;
        }
    }
}