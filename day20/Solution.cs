using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace day20
{
    public class Solution
    {
        const long DECRYPTION_KEY = 811589153;
        public int PartOne(bool test)
        {
            LinkedList<int> filedata = new LinkedList<int>(
                GetInput(test).Select(x => int.Parse(x))
            );
            List<LinkedListNode<int>> originalList = new List<LinkedListNode<int>>();
            var currNode = filedata.First;
            LinkedListNode<int> zeroNode = null;
            while (currNode is not null)
            {
                originalList.Add(currNode);
                if (currNode.Value == 0)
                    zeroNode = currNode;
                currNode = currNode.Next;
            }
            for (int i = 0; i < originalList.Count; ++i)
            {
                //idx for 30 should be 3
                // the -30 should go at the end (8)
                var number = originalList[i];
                var indexInData = filedata.FindIndexOfNode(number);
                var newIndex = indexInData.index + number.Value;
                if (newIndex == 0) //moving the third number 2 places back doesn't make it the first number but the last.... i don't get the logic
                {
                    var index = originalList.Count -1;
                    filedata.Remove(indexInData.node);
                    filedata.InsertAtIndex(indexInData.node, index);
                }
                else if (newIndex < 0)
                {
                    var timesRound = (int)Math.Floor((decimal)Math.Abs(newIndex) / (originalList.Count-1));
                    var normalized = (Math.Abs(newIndex) + timesRound) % (originalList.Count);
                    var index = originalList.Count - normalized -1;
                    filedata.Remove(indexInData.node);
                    filedata.InsertAtIndex(indexInData.node, index);
                }
                else if (newIndex > originalList.Count -1)
                {
                    var timesRound = (int)Math.Floor((decimal)Math.Abs(newIndex) / (originalList.Count-1));
                    var index = (newIndex +timesRound) % (originalList.Count); //yay for hidden reqs
                    filedata.Remove(indexInData.node);
                    filedata.InsertAtIndex(indexInData.node, index);
                }
                else
                {
                    filedata.Remove(indexInData.node);
                    filedata.InsertAtIndex(indexInData.node, newIndex);
                }
            }
            //look at index 1000, 2000, 3000 AFTER 0 (the number not the index)
            var zeroIndex = filedata.FindIndexOfNode(zeroNode!).index;
            var indices = new[] {1000, 2000, 3000}.Select(x => (x+zeroIndex) % originalList.Count);
            var ezlookup = new List<int>(filedata);
            return indices.Select(x => ezlookup[x]).Sum();
        }

        public long PartTwo(bool test)
        {
            LinkedList<long> filedata = new LinkedList<long>(
                GetInput(test).Select(x => checked(long.Parse(x)*DECRYPTION_KEY))
            );
            List<LinkedListNode<long>> originalList = new List<LinkedListNode<long>>();
            var currNode = filedata.First;
            LinkedListNode<long> zeroNode = null;
            while (currNode is not null)
            {
                originalList.Add(currNode);
                if (currNode.Value == 0)
                    zeroNode = currNode;
                currNode = currNode.Next;
            }
            for (int letimes = 0; letimes < 10; ++letimes)
            {
                for (int i = 0; i < originalList.Count; ++i)
                {
                    //idx for 30 should be 3
                    // the -30 should go at the end (8)
                    var number = originalList[i];
                    var indexInData = filedata.FindIndexOfNode(number);
                    var newIndex = (long)indexInData.index + number.Value;
                    if (newIndex == indexInData.index)
                        continue;
                    if (newIndex == 0) //moving the third number 2 places back doesn't make it the first number but the last.... i don't get the logic
                    {
                        var index = originalList.Count -1;
                        filedata.Remove(indexInData.node);
                        filedata.InsertAtIndex(indexInData.node, index);
                    }
                    if (newIndex == originalList.Count -1) //wrap around
                    {
                        var index = 0;
                        filedata.Remove(indexInData.node);
                        filedata.InsertAtIndex(indexInData.node, index);
                    }
                    else if (newIndex < 0)
                    {
                        var timesRound = (long)Math.Floor((decimal)Math.Abs(newIndex) / (originalList.Count-1));
                        var normalized = checked((Math.Abs(newIndex) + timesRound)) % (originalList.Count);
                        var index = originalList.Count - normalized -1;
                        filedata.Remove(indexInData.node);
                        filedata.InsertAtIndex(indexInData.node, index);
                    }
                    else if (newIndex > originalList.Count -1)
                    {
                        var timesRound = (long)Math.Floor((decimal)Math.Abs(newIndex) / (originalList.Count-1));
                        var index = checked((newIndex +timesRound)) % (originalList.Count); //yay for hidden reqs
                        filedata.Remove(indexInData.node);
                        filedata.InsertAtIndex(indexInData.node, index);
                    }
                    else
                    {
                        filedata.Remove(indexInData.node);
                        filedata.InsertAtIndex(indexInData.node, newIndex);
                    }
                }
            }
            //look at index 1000, 2000, 3000 AFTER 0 (the number not the index)
            var zeroIndex = filedata.FindIndexOfNode(zeroNode!).index;
            var indices = new[] {1000, 2000, 3000}.Select(x => (x+zeroIndex) % originalList.Count);
            var ezlookup = new List<long>(filedata);
            return indices.Select(x => ezlookup[x]).Sum();
        }

        public string[] GetInput(bool test)
        {
            string filename = test ? "input" : "input_full";
            string path = $"/mnt/dev/Learning/AoC/Days/day20/{filename}";
            return System.IO.File.ReadAllLines(path);
        }
    }

    public static class LinkedListExtension
    {
        public static (int index, LinkedListNode<int> node) FindIndexOfNode(this LinkedList<int> list, LinkedListNode<int> item)
        {
            int i = 0;
            var current = list.First;
            if (current is null) return (-1, null!);
            while (current is not null)
            {
                if (current == item)
                {
                    return (i, current);
                }
                current = current.Next;
                ++i;
            }
            return (-1, null!);
        }

        public static (int index, LinkedListNode<long> node) FindIndexOfNode(this LinkedList<long> list, LinkedListNode<long> item)
        {
            int i = 0;
            var current = list.First;
            if (current is null) return (-1, null!);
            while (current is not null)
            {
                if (current == item)
                {
                    return (i, current);
                }
                current = current.Next;
                ++i;
            }
            return (-1, null!);
        }

        public static void InsertAtIndex(this LinkedList<long> list, LinkedListNode<long> node, long index)
        {
            if (index == 0)
            {
                list.AddFirst(node);
                return;
            }
            if (index == list.Count)
            {
                list.AddLast(node);
                return;
            }
            if (index < 0 || index > list.Count) throw new ArgumentException();
            var current = list.First;
            for (int i = 0; i < index -1; ++i)
            {
                current = current.Next;
            }
            list.AddAfter(current, node);
        }

        public static void InsertAtIndex(this LinkedList<int> list, LinkedListNode<int> node, int index)
        {
            if (index == 0)
            {
                list.AddFirst(node);
                return;
            }
            if (index == list.Count)
            {
                list.AddLast(node);
                return;
            }
            if (index < 0 || index > list.Count) throw new ArgumentException();
            var current = list.First;
            for (int i = 0; i < index -1; ++i)
            {
                current = current.Next;
            }
            list.AddAfter(current, node);
        }
    }
}