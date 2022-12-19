global using static System.Console;
namespace day17;

public class Program
{

public static void Main()
{
    Solution s = new Solution();
    D17.RunP2(s.GetInput(true)[0]);
    WriteLine(s.partone(true));
    WriteLine(s.partone(false));
    WriteLine("part two answers: ");
    WriteLine(s.partTwo(true));
    WriteLine(s.partTwo(false));

}
}
