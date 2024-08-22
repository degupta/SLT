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
