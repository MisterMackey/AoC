using static System.Console;

namespace day11;

public class UnitTest1
{
    [Fact]
    public void Test1()
    {
        WriteLine("Test input part 1");
        var p = new Program();
        p.Run(true, true);
    }

    [Fact]
    public void FullTest()
    {
        WriteLine("Full input part 1");
        var p =new Program();
        p.Run(false, true);
    }

    [Fact]
    public void test2()
    {
        WriteLine("Test input part 2");
        var p = new Program();
        p.Run(true, false);
    }

    [Fact]
    public void full2()
    {
        WriteLine("Full input part 2");
        var p = new Program();
        p.Run(false, false);
    }
}