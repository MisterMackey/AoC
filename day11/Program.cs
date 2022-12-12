using System;
using System.Linq.Expressions;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Text.RegularExpressions;
using static System.Console;

namespace day11
{
    public class Program
    {
        public void Run(bool test = true, bool partone = true)
        {
            var input = ReadFile(test);
            input.Add(""); //cuz system io is an a-hole and trims the last line for some reason
            var monkeysUnparsed = SplitMonkeys(input);
            List<Monkey> monkeys = new List<Monkey>();
            double maxDivision = 1;
            foreach (var um in monkeysUnparsed)
            {
                var m = FormMonkey(um, monkeys);
                monkeys.Add(m);
                maxDivision *= m.Divisor;
            }
            int numRounds = partone ? 20 : 10000;
            for (int i =0; i < numRounds; i++)
            {
                PlayRound(monkeys, maxDivision, partone);
            }
            WriteLine("Total inspections:");
            foreach (var m in monkeys)
            {
                WriteLine($"{m.Name}: {m.InspectionCount}");
            }
            var sorted = monkeys.OrderBy(x => x.InspectionCount).Reverse().ToList();
            WriteLine($"Monkey business: {sorted[0].InspectionCount * sorted[1].InspectionCount}");
        }

        public void PlayRound(List<Monkey> l, double maxDivision, bool partone)
        {
            foreach (Monkey m in l)
            {
                m.TakeTurn(maxDivision, partone);
            }
        }

        List<string> ReadFile(bool test)
        {
            string fileName = test ? "input" : "input_full";
            var path = $"/mnt/dev/Learning/AoC/Days/day11/{fileName}";
            var lines = System.IO.File.ReadAllLines(path);
            return lines.ToList();
        }

        List<List<string>> SplitMonkeys(List<string> lines)
        {
            int i = 0;
            //kek
            List<List<string>> ret = new List<List<string>>();
            List<string> current = new List<string>();
            foreach (var line in lines)
            {
                if (i < 6)
                {
                    ++i;
                    current.Add(line);
                }
                else
                {
                    i = 0;
                    ret.Add(current);
                    current = new List<string>();
                }
            }
            return ret;
        }

        Monkey FormMonkey(List<string> input, List<Monkey> fullList)
        {
            var name = input[0].Replace(":", "");
            var items = input[1].Split(":")[1].Split(",").Select(
                x => double.Parse(x)
            ).ToList();
            var operationCode = input[2].Split(":")[1];
            var monkeyOperation = FormOperation(operationCode.Trim());
            var testCode = input[3].Split(":")[1];
            var monkeyTest = FormTest(testCode);
            var monkeyAction = FormAction(input[4], input[5], fullList);
            return new Monkey(
                name,
                items,
                monkeyOperation,
                monkeyTest.Item2,
                monkeyAction
            ) {Divisor = monkeyTest.Item1};
        }

        private Action<bool, double> FormAction(string tr, string fa, List<Monkey> list)
        {
            //just get the index out with regex and create a closure for it (and pray to not get indexoutofrange at runtime)
            Regex re = new Regex(@"\d+");
            var numTrue = re.Match(tr);
            var pNumTrue = int.Parse(numTrue.Groups[0].Value);
            var numFalse = re.Match(fa);
            var pNumFalse = int.Parse(numFalse.Groups[0].Value);
            return (bool x, double y) => 
            {
                if (x)
                    list[pNumTrue].items.Add(y);
                else
                    list[pNumFalse].items.Add(y);
            };
        }

        private (int, Func<double, bool>) FormTest(string testcode)
        {
            Regex re = new Regex(@"\d+");
            var m = re.Match(testcode);
            var number = m.Groups[0].Value;
            var pnumber = int.Parse(number);
            return (pnumber, x => x % pnumber == 0);
        }

        private Func<double,double> FormOperation(string operationCode)
        {
            var tokens = operationCode.Split(" ");
            //tokens takes following form:
            // {output_name} = {operand} {operator} {operand}
            // it is always a mapping from int to int
            ParameterExpression left = Expression.Parameter(typeof(double), "old");
            Expression right = tokens[4] switch
            {
                "old" => left,
                _ => Expression.Constant(double.Parse(tokens[4]), typeof(double))
            };
            var mOperator = tokens[3] switch
            {
                "*" => Expression.Multiply(left, right),
                "+" => Expression.Add(left, right),
                "-" => Expression.Subtract(left, right),
                "/" => Expression.Divide(left, right),
                _ => throw new Exception("g wat?")
            };
            var MonkeyOperation = Expression.Lambda<Func<double, double>>(
                mOperator,
                parameters: new ParameterExpression[] { left }
            ).Compile();
            return MonkeyOperation;
        }
    }
}