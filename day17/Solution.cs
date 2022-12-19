using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace day17
{
    public class Solution
    {
        public int partone(bool test)
        {
            var input = GetInput(test)[0];
            Queue<char> jets = new Queue<char>();
            foreach (char x in input.AsEnumerable())
            {
                jets.Enqueue(x=='<' ? 'L': 'R');
            }
            List<List<byte>> chamber = new List<List<byte>>(7);
            for (int i =0; i < 7; i++)
            {
                chamber.Add(new List<byte>(1000*1000) {1});
                for (int j =1; j< 1000*1000; ++j)
                {
                    chamber[i].Add(0);
                }
            }
            bool WillCollide(List<List<byte>> chamber, List<List<byte>> block, char direction, int yoffset)
            {
                switch (direction)
                {
                    case 'L':
                        if (block[0].Any(x => x ==1))
                            return true;
                        return Enumerable.Range(1,6).Any(i => 
                        {
                            return Enumerable.Range(0,4).Any(j => block[i][j] == 1 && chamber[i-1][j+yoffset] == 1);
                        });
                    case 'R':
                        if (block[6].Any(x => x ==1))
                            return true;
                        return Enumerable.Range(0,6).Any(i => 
                        {
                            return Enumerable.Range(0,4).Any(j => block[i][j] == 1 && chamber[i+1][j+yoffset] == 1);
                        });
                    case 'D':
                        if (yoffset == 1) //floor would be hit
                            return true;
                        return Enumerable.Range(0,7).Any(i => 
                        {
                            return Enumerable.Range(0,4).Any(j => block[i][j] == 1 && chamber[i][j+yoffset-1] == 1);
                        });
                    default: throw new Exception();
                }
            }
            int currentHeight = 0;
            int blocksAtRest = 0;
            int blockLimit = 2022;
            var shapeCollection = new Shapes().GetEnumerator();
            var directions = new Directions(jets).GetEnumerator();
            var heights = new int[] {1,3,3,4,2};
            while (blocksAtRest < blockLimit)
            {
                int currentBlockYOffset = currentHeight + 4;
                //spawn block
                shapeCollection.MoveNext();
                var shape = shapeCollection.Current;
                //move block 3 spaces down (do not check for down collision)
                MoveBlockJet(shape, currentBlockYOffset);
                --currentBlockYOffset;
                MoveBlockJet(shape, currentBlockYOffset);
                --currentBlockYOffset;
                MoveBlockJet(shape, currentBlockYOffset);
                --currentBlockYOffset;
                //move block until collision detected
                MoveBlockJet(shape, currentBlockYOffset);
                while (!WillCollide(chamber, shape, 'D', currentBlockYOffset))
                {
                    --currentBlockYOffset;
                    MoveBlockJet(shape, currentBlockYOffset);
                }
                for (int i=0; i< 7; ++i)
                {
                    for (int j = 0; j < 4; ++j)
                    {
                        if (shape[i][j] == 1)
                        {
                            chamber[i][j+currentBlockYOffset] = shape[i][j];
                        }
                    }
                }
                var absoluteShapeHeight = heights[blocksAtRest % 5] + currentBlockYOffset -1;
                currentHeight = currentHeight > absoluteShapeHeight ? currentHeight : absoluteShapeHeight;
                blocksAtRest++;
            }
            //checks for collision
            void MoveBlockJet(List<List<byte>> block, int y_offset)
            {
                directions.MoveNext();
                var dir = directions.Current;
                var collision = WillCollide(chamber, block, dir, y_offset);
                if (collision)
                    return;
                if (dir == 'L')
                {
                    for (int i = 0; i < 6; ++i)
                    {
                        block[i] = block[i+1];
                    }
                    block[6] = new List<byte>{0,0,0,0};
                }
                else
                {
                    for (int i = 6; i > 0; --i)
                    {
                        block[i] = block[i-1];
                    }
                    block[0] = new List<byte>{0,0,0,0};
                }

            }
            return currentHeight;
        }

        public class Directions : IEnumerable<char>
        {
            public Queue<char> Input { get; }
            public Directions(Queue<char> input)
            {
            this.Input = input;

            }
            public IEnumerator<char> GetEnumerator()
            {
                while (true)
                {
                    var item = Input.Dequeue();
                    yield return item;
                    Input.Enqueue(item);
                }
            }

            IEnumerator IEnumerable.GetEnumerator()
            {
                return GetEnumerator();
            }
        }

        public class Shapes : IEnumerable<List<List<byte>>>
        {
            public IEnumerator<List<List<byte>>> GetEnumerator()
            {
                Queue<List<List<byte>>> shapes = new Queue<List<List<byte>>>();
                shapes.Enqueue(new List<List<byte>>
                {
                    new List<byte>{0,0,0,0},
                    new List<byte>{0,0,0,0},
                    new List<byte>{1,0,0,0},
                    new List<byte>{1,0,0,0},
                    new List<byte>{1,0,0,0},
                    new List<byte>{1,0,0,0},
                    new List<byte>{0,0,0,0},
                });
                shapes.Enqueue(new List<List<byte>>
                {
                    new List<byte>{0,0,0,0},
                    new List<byte>{0,0,0,0},
                    new List<byte>{0,1,0,0},
                    new List<byte>{1,1,1,0},
                    new List<byte>{0,1,0,0},
                    new List<byte>{0,0,0,0},
                    new List<byte>{0,0,0,0},
                });
                shapes.Enqueue(new List<List<byte>>
                {
                    new List<byte>{0,0,0,0},
                    new List<byte>{0,0,0,0},
                    new List<byte>{1,0,0,0},
                    new List<byte>{1,0,0,0},
                    new List<byte>{1,1,1,0},
                    new List<byte>{0,0,0,0},
                    new List<byte>{0,0,0,0},
                });
                shapes.Enqueue(new List<List<byte>>
                {
                    new List<byte>{0,0,0,0},
                    new List<byte>{0,0,0,0},
                    new List<byte>{1,1,1,1},
                    new List<byte>{0,0,0,0},
                    new List<byte>{0,0,0,0},
                    new List<byte>{0,0,0,0},
                    new List<byte>{0,0,0,0},
                });
                shapes.Enqueue(new List<List<byte>>
                {
                    new List<byte>{0,0,0,0},
                    new List<byte>{0,0,0,0},
                    new List<byte>{1,1,0,0},
                    new List<byte>{1,1,0,0},
                    new List<byte>{0,0,0,0},
                    new List<byte>{0,0,0,0},
                    new List<byte>{0,0,0,0},
                });

                while (true)
                {
                    var nextShape = shapes.Dequeue();
                    var item = new List<List<byte>>
                    {
                        new List<byte>(nextShape[0]),
                        new List<byte>(nextShape[1]),
                        new List<byte>(nextShape[2]),
                        new List<byte>(nextShape[3]),
                        new List<byte>(nextShape[4]),
                        new List<byte>(nextShape[5]),
                        new List<byte>(nextShape[6])
                    };
                    yield return item;
                    shapes.Enqueue(nextShape);
                }
            }

            IEnumerator IEnumerable.GetEnumerator()
            {
                return GetEnumerator();
            }
        }

        public string[] GetInput(bool test)
        {
            string filename = test ? "input" : "input_full";
            string path = $"/mnt/dev/Learning/AoC/Days/day17/{filename}";
            return System.IO.File.ReadAllLines(path);
        }

        public long partTwo(bool test)
        {
            var input = GetInput(test)[0];
            Queue<char> jets = new Queue<char>();
            foreach (char x in input.AsEnumerable())
            {
                jets.Enqueue(x=='<' ? 'L': 'R');
            }
            List<List<byte>> chamber = new List<List<byte>>(7);
            for (int i =0; i < 7; i++)
            {
                chamber.Add(new List<byte>(100*1000*1000) {1});
                for (int j =1; j< 100*1000*1000; ++j)
                {
                    chamber[i].Add(0);
                }
            }
            bool WillCollide(List<List<byte>> chamber, List<List<byte>> block, char direction, int yoffset)
            {
                switch (direction)
                {
                    case 'L':
                        if (block[0].Any(x => x ==1))
                            return true;
                        return Enumerable.Range(1,6).Any(i => 
                        {
                            return Enumerable.Range(0,4).Any(j => block[i][j] == 1 && chamber[i-1][j+yoffset] == 1);
                        });
                    case 'R':
                        if (block[6].Any(x => x ==1))
                            return true;
                        return Enumerable.Range(0,6).Any(i => 
                        {
                            return Enumerable.Range(0,4).Any(j => block[i][j] == 1 && chamber[i+1][j+yoffset] == 1);
                        });
                    case 'D':
                        if (yoffset == 1) //floor would be hit
                            return true;
                        return Enumerable.Range(0,7).Any(i => 
                        {
                            return Enumerable.Range(0,4).Any(j => block[i][j] == 1 && chamber[i][j+yoffset-1] == 1);
                        });
                    default: throw new Exception();
                }
            }
            int currentHeight = 0;
            int blocksAtRest = 0;
            int blockLimit = int.MaxValue;
            var shapeCollection = new Shapes().GetEnumerator();
            var directions = new Directions(jets).GetEnumerator();
            var heights = new int[] {1,3,3,4,2};
            int jetBlasts = 0;
            List<long> heightAtBlockCount = new List<long>{0};
            int blockIndex = 0;
            while (blocksAtRest < blockLimit)
            {
                //check for repetition
                int currentBlockYOffset = checked(currentHeight + 4);
                //spawn block
                shapeCollection.MoveNext();
                var shape = shapeCollection.Current;
                //move block 3 spaces down (do not check for down collision)
                MoveBlockJet(shape, currentBlockYOffset);
                --currentBlockYOffset;
                MoveBlockJet(shape, currentBlockYOffset);
                --currentBlockYOffset;
                MoveBlockJet(shape, currentBlockYOffset);
                --currentBlockYOffset;
                //move block until collision detected
                MoveBlockJet(shape, currentBlockYOffset);
                while (!WillCollide(chamber, shape, 'D', currentBlockYOffset))
                {
                    --currentBlockYOffset;
                    MoveBlockJet(shape, currentBlockYOffset);
                }
                for (int i=0; i< 7; ++i)
                {
                    for (int j = 0; j < 4; ++j)
                    {
                        if (shape[i][j] == 1)
                        {
                            chamber[i][j+currentBlockYOffset] = shape[i][j];
                        }
                    }
                }
                var absoluteShapeHeight = heights[blocksAtRest % 5] + currentBlockYOffset -1;
                currentHeight = currentHeight > absoluteShapeHeight ? currentHeight : absoluteShapeHeight;
                blocksAtRest++;
                heightAtBlockCount.Add(currentHeight);

                blockIndex = (blockIndex + 1) % 5;
                //todo, let the jetblasts index be any number, i.e. let the repeat happen in the middle of the sequence if need be.
                if (jetBlasts == 0 && blockIndex == 0)
                {
                    bool check = false;
                    if (check)
                    {
                        //pattern detected! :D
                        var heightOfPattern = heightAtBlockCount[blocksAtRest];
                        var numblocksInPattern = blocksAtRest;
                        long partTwoLimit = 1000000000000;
                        var patternRepeats = partTwoLimit / numblocksInPattern;
                        var heightInRepeats = checked(patternRepeats*heightOfPattern);
                        var remainder = (int)(partTwoLimit % numblocksInPattern);
                        var remainingHeight = heightAtBlockCount[remainder];
                        return checked(heightInRepeats + remainingHeight);
                    }
                }
            }
            //checks for collision
            void MoveBlockJet(List<List<byte>> block, int y_offset)
            {
                directions.MoveNext();
                var dir = directions.Current;
                jetBlasts = (jetBlasts + 1) % input.Length;
                var collision = WillCollide(chamber, block, dir, y_offset);
                if (collision)
                    return;
                if (dir == 'L')
                {
                    for (int i = 0; i < 6; ++i)
                    {
                        block[i] = block[i+1];
                    }
                    block[6] = new List<byte>{0,0,0,0};
                }
                else
                {
                    for (int i = 6; i > 0; --i)
                    {
                        block[i] = block[i-1];
                    }
                    block[0] = new List<byte>{0,0,0,0};
                }

            }
            throw new Exception("no pattern could be found");
        }
    }
}