-module(SLAU).
-export([main/1]).


main(_) ->
    Inp1 = case io:fread("First the flag: ", "~s") of
        {ok, [R|_]} -> R;
        {error, _}  ->
            io:format("Error while reading your string"),
            erlang:exit(error_read)
    end,
    Inp2 = case io:fread("Second the flag: ", "~s") of
        {ok, [S|_]} -> S;
        {error, _}  ->
            io:format("Error while reading your string"),
            erlang:exit(error_read)
    end,
    Inp3 = case io:fread("Third the flag: ", "~s") of
        {ok, [T|_]} -> T;
        {error, _}  ->
            io:format("Error while reading your string"),
            erlang:exit(error_read)
    end,
    Inp4 = case io:fread("Fourth the flag: ", "~s") of
        {ok, [V|_]} -> V;
        {error, _}  ->
            io:format("Error while reading your string"),
            erlang:exit(error_read)
    end,
    Inp5 = case io:fread("Fifth the flag: ", "~s") of
        {ok, [W|_]} -> W;
        {error, _}  ->
            io:format("Error while reading your string"),
            erlang:exit(error_read)
    end,
    Process1 = fun(A) -> (A - hd("a") + 12) rem 26 + hd("a") end,
    Processed1 = lists:map(Process1, Inp1),
    Process2 = fun(A) -> (A - hd("a") + 7) rem 26 + hd("a") end,
    Processed2 = lists:map(Process2, Inp2),
    Process3 = fun(A) -> (A - hd("a") + 9) rem 26 + hd("a") end,
    Processed3 = lists:map(Process3, Inp3),
    Process4 = fun(A) -> (A - hd("a") + 21) rem 26 + hd("a") end,
    Processed4 = lists:map(Process4, Inp4),
    Process5 = fun(A) -> (A - hd("a") + 22) rem 26 + hd("a") end,
    Processed5 = lists:map(Process5, Inp5),
    case string:equal(Processed1, "qdxmzsue") and string:equal(Processed2, "aolilza") and string:equal(Processed3, "yaxpajvvrwp") and string:equal(Processed4, "gvibpvbz") and string:equal(Processed5, "atyalpxb") of
        true  -> io:format("Right\n");
        false -> io:format("Wrong\n")
    end.
