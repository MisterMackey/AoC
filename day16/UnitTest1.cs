using System.Diagnostics;
namespace day16;

public class UnitTest1
{
    [Fact]
    public void PartOneTest()
    {
        var s = new Solution();
        Stopwatch sw = new Stopwatch();
        sw.Start();
        var answer = s.PartOne(true);
        sw.Stop();
        Assert.Equal(expected: 1651, actual:answer);
        Console.WriteLine($"Answer for test par tone: {answer}. Calculated in {sw.Elapsed.Seconds} seconds");
    }

    [Fact]
    public void PartOneFull()
    {
        var s = new Solution();
        Stopwatch sw = new Stopwatch();
        sw.Start();
        var answer = s.PartOne(false);
        Console.WriteLine($"Answer for full part one: {answer}. Calculated in {sw.Elapsed.Seconds} seconds");
    }

    [Fact]
    public void PartTwoTest()
    {
        var s = new Solution();
        Stopwatch sw = new Stopwatch();
        sw.Start();
        var answer = s.PartTwo(true);
        Assert.Equal(expected: 1707, actual:answer);
        Console.WriteLine($"Answer for test part two: {answer}. Calculated in {sw.Elapsed.Seconds} seconds");
    }

    [Fact]
    public void PartTwoFull()
    {
        var s = new Solution();
        Stopwatch sw = new Stopwatch();
        sw.Start();
        var answer = s.PartTwo(false);
        Console.WriteLine($"Answer for full part two: {answer}. Calculated in {sw.Elapsed.Seconds} seconds");
    }

    private void runthisshit()
    {
    }
}