import grpc
import game_pb2
import game_pb2_grpc

PLAYER_1 = "p1"
PLAYER_2 = "p2"

channel = grpc.insecure_channel("localhost:5051")
client = game_pb2_grpc.GameServiceStub(channel)

def get_game(id):
    return client.GetGame(game_pb2.GetGameRequest(gameId=id))

def create_new_game():
    return client.CreateGame(game_pb2.CreateGameRequest(player1=PLAYER_1, player2=PLAYER_2)).game

def test_create_game():
    game = create_new_game()
    assert len(game.gameId) == 36
    assert game.player1 == PLAYER_1
    assert game.player2 == PLAYER_2
    assert game.firstPlayerInnings
    assert game.firstInnings.score == 0
    assert game.firstInnings.wickets == 0
    assert game.firstInnings.balls == 0

    game2 = get_game(game.gameId)
    assert game == game2

def test_get_game():
    g = create_new_game()
    assert g == get_game(g.gameId)


def play_ball(game_id, type, runs, batsmen, bowler):
    return client.PlayBall(game_pb2.PlayBallRequest(gameId=game_id, ballerEvent=game_pb2.BallEvent(
        type = type, ballerName = bowler, batsmenName=batsmen, runsScored=runs
    )))

def assert_game_status(game, num, score, balls, wickets):
    assert len(game.balls) == num
    assert game.firstInnings.score == score
    assert game.firstInnings.balls == balls
    assert game.firstInnings.wickets == wickets

def test_playing_a_ball():
    game = create_new_game()
    game_id = game.gameId
    assert len(game.balls) == 0
    
    play_ball(game_id, game_pb2.Normal, 2, PLAYER_1, PLAYER_2)
    g = get_game(game_id)
    assert_game_status(g, 1, 2, 1, 0)

    play_ball(game_id, game_pb2.Normal, 1, PLAYER_1, PLAYER_2)
    g = get_game(game_id)
    assert_game_status(g, 2, 3, 2, 0)

    play_ball(game_id, game_pb2.Wicket, 0, PLAYER_1, PLAYER_2)
    g = get_game(game_id)
    assert_game_status(g, 3, 3, 3, 1)

    play_ball(game_id, game_pb2.Wide, 0, PLAYER_1, PLAYER_2)
    g = get_game(game_id)
    assert_game_status(g, 4, 4, 3, 1)

    play_ball(game_id, game_pb2.NoBall, 1, PLAYER_1, PLAYER_2)
    g = get_game(game_id)
    assert_game_status(g, 5, 6, 3, 1)
