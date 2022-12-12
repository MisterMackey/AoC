using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace day11
{
    public class Monkey
    {
        public string Name { get; }
        public long InspectionCount {get; private set;}
        public List<double> items {get; private set;}
        private readonly Func<double, double> operation;
        private readonly Func<double, bool> test;
        private readonly Action<bool, double> action;
        public int Divisor {get; set; }

        public Monkey(string name,
            List<double> items,
            Func<double, double> operation,
            Func<double, bool> test,
            Action<bool, double> action)
        {
            Name = name;
            this.items = items;
            this.operation = operation;
            this.test = test;
            this.action = action;
            this.InspectionCount = 0;
        }

        double PostInspect(double x)
        {
            return Math.Floor(x/3);
        }

        public void TakeTurn(double maxDivision, bool partone)
        {
            foreach (var item in items)
            {
                var newVal = operation(item);
                if (partone)
                    newVal = PostInspect(newVal);
                else
                    newVal = newVal % maxDivision;
                var testResult = test(newVal);
                action(testResult, newVal);
                InspectionCount++;
            }
            items.Clear();
        }
    }
}