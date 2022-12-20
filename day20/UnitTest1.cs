namespace day20;

public class UnitTest1
{
    [Fact]
    public void PartOne_Test()
    {
        var s = new Solution();
        var answer = s.PartOne(true);
        Console.WriteLine(answer);
        Assert.Equal(3, answer);
    }

    [Fact]
    public void PartOne_Full()
    {
        var s = new Solution();
        var answer = s.PartOne(false);
        Console.WriteLine(answer);
        Assert.Equal(2215, answer);
    }

    [Fact]
    public void PartTwo_Test()
    {
        var s = new Solution();
        var answer = s.PartTwo(true);
        Console.WriteLine(answer);
        Assert.Equal(1623178306, answer);
    }

    [Fact]
    public void PartTwo_Full()
    {
        var s = new Solution();
        var answer = s.PartTwo(false);
        Console.WriteLine(answer);
    }
}