using System.Xml.Serialization;
using System.ComponentModel.DataAnnotations;
using System.Text.RegularExpressions;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace day16
{
    public class Solution
    {
        private const int answerListSize = 1000*1000*100;
        private List<(Stack<Room> guyPath, Stack<Room> elephantPath, int score)> centralListOfPaths;
        private SpinLock spinlock;
        private ulong paths =0;
        public int PartOne(bool test)
        {
            var input = GetInput(test);
            var rooms = ParseInput(input);
            var distances = new Dictionary<string, Dictionary<string,int>>();
            foreach (var room in rooms)
            {
                Dictionary<string, int> distanceTo = new Dictionary<string, int>();
                foreach (var n_room in rooms)
                {
                    distanceTo.Add(n_room.name, 0);
                }
                distances.Add(room.name, distanceTo);
            }
            List<Room> q = new List<Room>(rooms);
            foreach (var room in rooms)
            {
                q.Remove(room);
                foreach (var target in q)
                {
                    var distanceTo = Dijkstra(room, target, rooms);
                    distances[room.name][target.name] = distanceTo;
                    distances[target.name][room.name] = distanceTo;
                }
            }
            var roomsToBotherWith = rooms.Where(x => x.flowRate > 0).ToList();
            int timeLimit = 30;

            var firstRoom = new Stack<Room>();
            firstRoom.Push(rooms.First(x => x.name == "AA"));
            var AllPossiblePaths = CalculateNextPossibleSteps(0, timeLimit, firstRoom, roomsToBotherWith, distances);
            var biggestRelease = AllPossiblePaths.MaxBy(x => x.score);
            return biggestRelease.score;
        }

        public int PartTwo(bool test, int timeConstraint)
        {
            var input = GetInput(test);
            var rooms = ParseInput(input);
            var distances = new Dictionary<string, Dictionary<string,int>>();
            foreach (var room in rooms)
            {
                Dictionary<string, int> distanceTo = new Dictionary<string, int>();
                foreach (var n_room in rooms)
                {
                    distanceTo.Add(n_room.name, 0);
                }
                distances.Add(room.name, distanceTo);
            }
            List<Room> q = new List<Room>(rooms);
            foreach (var room in rooms)
            {
                q.Remove(room);
                foreach (var target in q)
                {
                    var distanceTo = Dijkstra(room, target, rooms);
                    distances[room.name][target.name] = distanceTo;
                    distances[target.name][room.name] = distanceTo;
                }
            }
            spinlock = new SpinLock();
            var extraspinlock = new SpinLock();
            int counter = 0;
            var roomsToBotherWith = rooms.Where(x => x.flowRate > 0).ToList();
            int timeLimit = 26;
            centralListOfPaths = new List<(Stack<Room> guyPath, Stack<Room> elephantPath, int score)>(answerListSize);
            var firstRoom = new Stack<Room>();
            firstRoom.Push(rooms.First(x => x.name == "AA"));
            //this works only if both actors run out of time and don't need to cooperate
            var AllPossiblePathsGuy = CalculateNextPossibleSteps(0, timeLimit, firstRoom, roomsToBotherWith, distances, timeConstraint);
            Console.WriteLine($"{AllPossiblePathsGuy.Count} paths to check");
            var bestPath = AllPossiblePathsGuy.MaxBy(x => x.score);
            int highscore = bestPath.score;
            Parallel.ForEach(AllPossiblePathsGuy,
            new ParallelOptions{MaxDegreeOfParallelism = 12},
            path =>
            {
                bool cacq = false;
                extraspinlock.TryEnter(ref cacq);
                if (cacq)
                {
                    counter++;
                    if (counter % 10000 ==0) Console.WriteLine($"done {counter}");
                    extraspinlock.Exit();
                }
                if (path.score < highscore/2)
                {
                    return;
                }
                //find the best path for the elephant given the path of the guy..
                var roomsLeft = roomsToBotherWith.Where(x => !path.Item1.Contains(x)).ToList();
                var allElephantPaths = CalculateNextPossibleSteps(path.score, timeLimit, firstRoom, roomsLeft, distances, 0);
                var bestElephantPathInThisCase = allElephantPaths.MaxBy(x => x.score);
                if (highscore > bestElephantPathInThisCase.score)
                {
                    return;
                }
                else
                {
                    bool acq = false;
                    spinlock.TryEnter(ref acq);
                    if (acq)
                    {
                        if (highscore < bestElephantPathInThisCase.score)
                        {
                            highscore = bestElephantPathInThisCase.score;
                        }
                        spinlock.Exit();
                    }
                }
            });
            return highscore;
        }

        private List<(Stack<Room>, Stack<Room>, int score)> ResizeAnswerList()
        {
            var tmp = centralListOfPaths;
            centralListOfPaths = new List<(Stack<Room> guyPath, Stack<Room> elephantPath, int score)>(answerListSize);
            return tmp;
        }

        private void PutAnswer((Stack<Room> guyPath, Stack<Room> elephantPath, int score) answer)
        {
            bool acquired = false;
            spinlock.TryEnter(ref acquired);
            if (acquired)
            {
                centralListOfPaths.Add(answer);
                if (++paths % 1000 == 0) Console.WriteLine($"calculated {paths} paths");
                if (centralListOfPaths.Count == answerListSize-1)
                {
                    var oldList = ResizeAnswerList();
                    spinlock.Exit();
                    var bestAnswerSoFar = oldList.MaxBy(x => x.score);
                    PutAnswer(bestAnswerSoFar);
                }
                else
                {
                    spinlock.Exit();
                }
            }
        }

        private List<(Stack<Room>, int score)> CalculateNextPossibleSteps(int runningScore,
                                                                        int timeRemaining,
                                                                        Stack<Room> visitedSoFar,
                                                                        List<Room> allRoomsToVisit,
                                                                        Dictionary<string,Dictionary<string,int>> distances,
                                                                        int extraTimeConstraint = 0)
        {
            var roomsToCheck = allRoomsToVisit.Where(x => !visitedSoFar.Contains(x)).ToList();
            if (timeRemaining <= (2+extraTimeConstraint)
                || roomsToCheck.Count == 0) //exit condition, no need to check anymore, just return the given list
            {
                //Console.WriteLine("Done 1 path");
                return new List<(Stack<Room>, int score)>() {(visitedSoFar, runningScore)};
            }
            List<(Stack<Room>, int score)> retlist = new List<(Stack<Room>, int score)>();
            foreach (var room in roomsToCheck)
            {
                var last = visitedSoFar.Peek();
                var visited = new Stack<Room>(new Stack<Room>(visitedSoFar));//shallow clone the path so far 
                visited.Push(room);
                int timeleft = timeRemaining - 1 -distances[last.name][room.name];
                if (timeleft < 0)
                {
                    visited.Pop();
                    retlist.Add((visitedSoFar, runningScore));
                }
                else
                {
                    int score = timeleft*room.flowRate + runningScore;
                    //REEECCUUURRRSSIIIIIOOOOON
                    var subPaths = CalculateNextPossibleSteps(score, timeleft, visited, allRoomsToVisit, distances, extraTimeConstraint);
                    retlist.AddRange(subPaths);
                }
            }
            return retlist;
        }

        private void CalculateNextPossibleStepsPartTwo(int runningScore,
                                                                        int guyTimeRemaining,
                                                                        int elephantTimeRemaining,
                                                                        Stack<Room> guyPath,
                                                                        Stack<Room> elephantPath,
                                                                        List<Room> allRoomsToVisit,
                                                                        Dictionary<string,Dictionary<string,int>> distances,
                                                                        bool rootCall = false,
                                                                        int callDepth = 0)
        {
            ++callDepth;
            if (callDepth > 20)
                Console.WriteLine($"something iffy with the recursion, call depth is {callDepth}");
            var roomsToCheck = allRoomsToVisit.Where(x => !guyPath.Contains(x) && !elephantPath.Contains(x)).ToList();
            if (roomsToCheck.Count == 0) //exit condition, no need to check anymore, just return the given list
            {
                //Console.WriteLine("Done 1 path");
                //pushing null refs so the stacks can be garbage collected since im running low on memory...
                PutAnswer((null!, null!, runningScore));
                return;
            }
            //early break
            if (guyTimeRemaining <= 2 && elephantTimeRemaining <= 2)
            {
                PutAnswer((null!, null!, runningScore));
                return;
            }
            if (rootCall)
            {
                Parallel.ForEach(roomsToCheck,
                new ParallelOptions {MaxDegreeOfParallelism = 6},
                room => 
                {
                    int score = runningScore;
                    int guyTimeLeft = guyTimeRemaining;
                    var guyVisited = guyPath;
                    //send the guy somewhere, provided he has time left
                    if (guyTimeRemaining <= 2)
                        goto elephantLogic; //Yes I had pasta for dinner, how could you tell?
                    var lastRoomOfGuy = guyPath.Peek();
                    guyVisited = new Stack<Room>(new Stack<Room>(guyPath));
                    guyTimeLeft = guyTimeRemaining - 1 -distances[lastRoomOfGuy.name][room.name];
                    if (guyTimeLeft < 0)
                    {
                        goto elephantLogic;
                    }
                    guyVisited.Push(room);
                    score = runningScore + guyTimeLeft*room.flowRate;

                    elephantLogic:
                    //send the elephant somewhere, provided it has time left
                    if (elephantTimeRemaining <= 2)
                    {
                        //nothing
                    }
                    else
                    {
                        //copy the rooms to check and remove the room we sent the guy to
                        var roomsToCheckForElephant = new List<Room>(roomsToCheck);
                        roomsToCheckForElephant.Remove(room);
                        //start sending the elephant everywhere and return the results
                        foreach (var elephantRoom in roomsToCheckForElephant)
                        {
                            var lastRoomOfElephant = elephantPath.Peek();
                            var elephantVisited = new Stack<Room>(new Stack<Room>(elephantPath));
                            int elephantTimeLeft = elephantTimeRemaining -1 -distances[lastRoomOfElephant.name][elephantRoom.name];
                            if (elephantTimeLeft < 0)
                            {
                                continue;
                            }
                            elephantVisited.Push(elephantRoom);
                            int scoreWithElephantIncluded = score + elephantTimeLeft*elephantRoom.flowRate;
                            CalculateNextPossibleStepsPartTwo(scoreWithElephantIncluded,
                                                                                guyTimeLeft,
                                                                                elephantTimeLeft,
                                                                                guyVisited,
                                                                                elephantVisited,
                                                                                allRoomsToVisit,
                                                                                distances, callDepth:callDepth);
                        }
                    }
                }
                );
            }
            else
            {
                foreach (var room in roomsToCheck)
                {
                    int score = runningScore;
                    int guyTimeLeft = guyTimeRemaining;
                    var guyVisited = guyPath;
                    //send the guy somewhere, provided he has time left
                    if (guyTimeRemaining <= 2)
                        goto elephantLogic; //Yes I had pasta for dinner, how could you tell?
                    var lastRoomOfGuy = guyPath.Peek();
                    guyVisited = new Stack<Room>(new Stack<Room>(guyPath));
                    guyTimeLeft = guyTimeRemaining - 1 -distances[lastRoomOfGuy.name][room.name];
                    if (guyTimeLeft < 0)
                    {
                        goto elephantLogic;
                    }
                    guyVisited.Push(room);
                    score = runningScore + guyTimeLeft*room.flowRate;

                    elephantLogic:
                    //send the elephant somewhere, provided it has time left
                    if (elephantTimeRemaining <= 2)
                    {
                        //nothing
                    }
                    else
                    {
                        //copy the rooms to check and remove the room we sent the guy to
                        var roomsToCheckForElephant = new List<Room>(roomsToCheck);
                        roomsToCheckForElephant.Remove(room);
                        //start sending the elephant everywhere and return the results
                        foreach (var elephantRoom in roomsToCheckForElephant)
                        {
                            var lastRoomOfElephant = elephantPath.Peek();
                            var elephantVisited = new Stack<Room>(new Stack<Room>(elephantPath));
                            int elephantTimeLeft = elephantTimeRemaining -1 -distances[lastRoomOfElephant.name][elephantRoom.name];
                            if (elephantTimeLeft < 0)
                            {
                                continue;
                            }
                            elephantVisited.Push(elephantRoom);
                            int scoreWithElephantIncluded = score + elephantTimeLeft*elephantRoom.flowRate;
                            CalculateNextPossibleStepsPartTwo(scoreWithElephantIncluded,
                                                                                guyTimeLeft,
                                                                                elephantTimeLeft,
                                                                                guyVisited,
                                                                                elephantVisited,
                                                                                allRoomsToVisit,
                                                                                distances, callDepth:callDepth);
                        }
                    }
                }
            }
            return;
        }

        private string[] GetInput(bool test)
        {
            string filename = test ? "input" : "input_full";
            string path = $"/mnt/dev/Learning/AoC/Days/day16/{filename}";
            return System.IO.File.ReadAllLines(path);
        }

        private List<Room> ParseInput(string[] input)
        {
            var rooms = input.Select(x => ParseRoom(x)).ToList();
            foreach (var room in rooms)
            {
                foreach (var adj in room.Adjacent_s)
                {
                    room.AdjacentRooms.Add(rooms.First(x => x.name == adj));
                }
            }
            return rooms;
        }

        private Room ParseRoom(string input)
        {
            var name = input.Substring(6,2);
            Regex flow = new Regex(@"flow rate=(\d+)");
            var flow_s = flow.Match(input);
            int flowrate = int.Parse(flow_s.Groups[1].Value);
            flow = new Regex("tunnels lead to valves (.+)");
            if (flow.IsMatch(input))
            {
                var adjacents_s = flow.Match(input);
                var ad = adjacents_s.Groups[1].Value.Replace(" ", "").Split(",").ToList();
                return new Room(name, flowrate) {Adjacent_s = ad};
            }
            else 
            {
                flow = new Regex(@"tunnel leads to valve (.{2})");
                var ad = flow.Match(input);
                return new Room(name,flowrate) {Adjacent_s = new List<string>() {ad.Groups[1].Value}};
            }
        }

        private int Dijkstra(Room start, Room target, List<Room> rooms)
        {
            var nodes = rooms.Select(x => new RoomNode(x, int.MaxValue)).ToList();
            var root = nodes.First(x => x.Room == start);
            root.Distance = 0;
            var end = nodes.First(x => x.Room == target);
            PriorityQueue<RoomNode, int> V = new PriorityQueue<RoomNode, int>();
            foreach (var node in nodes)
            {
                V.Enqueue(node, node.Distance);
            }
            List<RoomNode> visited = new List<RoomNode>();
            while (!visited.Contains(end) && V.Count != 0)
            {
                var current = V.Dequeue();
                foreach (var r in current.Room.AdjacentRooms)
                {
                    var nextNode = nodes.FirstOrDefault(x => x.Room == r);
                    if (nextNode is null)
                        continue; //node is in visited, skip
                    else
                    {
                        var dist = current.Distance + 1;
                        if (dist < nextNode.Distance)
                            nextNode.Distance = dist;
                    }
                }
                visited.Add(current);
                var tmp = new PriorityQueue<RoomNode, int>();
                while (V.Count != 0)
                {
                    var i = V.Dequeue();
                    tmp.Enqueue(i, i.Distance);
                }
                V = tmp;
            }
            return end.Distance;
        }
    }
}