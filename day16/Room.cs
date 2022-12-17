using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace day16
{
    public class Room
    {
        public string name {get; private set;}
        public int flowRate {get; private set;}
        public bool opened {get; set;}
        public List<Room> AdjacentRooms {get; } = new List<Room>();
        public List<string> Adjacent_s {get; set;}

        public Room(string name, int flowrate)
        {
            this.name = name;
            this.flowRate = flowrate;
            opened = false;
        }
    }
}