package controllers

import (
	"context"
	"encoding/json"
	"slt/pb"

	"github.com/google/uuid"
	redis "github.com/redis/go-redis/v9"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type GameController struct {
	Rdb *redis.Client
}

func (c *GameController) CreateGame(in *pb.CreateGameRequest) (*pb.CreateGameResponse, error) {
	game := &pb.Game{
		GameId:             uuid.New().String(),
		Player1:            in.Player1,
		Player2:            in.Player2,
		FirstPlayerInnings: true,
		FirstInnings:       &pb.InningsData{},
		SecondInnings:      &pb.InningsData{},
		Balls:              make([]*pb.BallEvent, 0),
		GameOver:           false,
		Winner:             "",
	}

	err := c.saveGame(game)
	if err != nil {
		return nil, status.Errorf(codes.Internal, err.Error())
	}

	return &pb.CreateGameResponse{Game: game}, nil
}

func (c *GameController) PlayBall(in *pb.PlayBallRequest) (*pb.Game, error) {
	game, err := c.getGame(in.GameId)
	if err != nil {
		return nil, status.Errorf(codes.Internal, err.Error())
	}

	if game == nil {
		return nil, status.Error(codes.NotFound, "Game Not Found")
	}

	if game.GameOver {
		return nil, status.Error(codes.InvalidArgument, "Game Already Over")
	}

	game.Balls = append(game.Balls, in.BallerEvent)
	innings := game.FirstInnings
	if !game.FirstPlayerInnings {
		innings = game.SecondInnings
	}

	switch in.BallerEvent.Type {
	case pb.BallType_Normal:
		if in.BallerEvent.RunsScored > 6 {
			return nil, status.Errorf(codes.InvalidArgument, "Cant score more than a six")
		}
		if in.BallerEvent.RunsScored < 0 {
			return nil, status.Errorf(codes.InvalidArgument, "Cant score less than a 0")
		}
		innings.Score += in.BallerEvent.RunsScored
		innings.Balls += 1
	case pb.BallType_Wicket:
		innings.Wickets += 1
		innings.Balls += 1
	case pb.BallType_NoBall:
		innings.Score += 1
		innings.Score += in.BallerEvent.RunsScored
	case pb.BallType_Wide:
		innings.Score += 1
		innings.Score += in.BallerEvent.RunsScored
	}

	c.checkEndOfGameOrInnings(game)

	err = c.saveGame(game)
	if err != nil {
		return nil, status.Errorf(codes.Internal, err.Error())
	}

	return game, nil
}

func (c *GameController) checkEndOfGameOrInnings(game *pb.Game) {
	innings := game.FirstInnings
	if !game.FirstPlayerInnings {
		innings = game.SecondInnings
	}

	if innings.Balls == 30 || innings.Wickets == 10 {

		if game.FirstPlayerInnings {
			game.FirstPlayerInnings = false
		} else {
			game.GameOver = true
			game.Winner = game.Player1
			if game.FirstInnings.Score < game.SecondInnings.Score {
				game.Winner = game.Player2
			}
		}
	}
}

func (c *GameController) GetGame(in *pb.GetGameRequest) (*pb.Game, error) {
	return c.getGame(in.GameId)
}

func (c *GameController) getGame(gameId string) (*pb.Game, error) {
	b, err := c.Rdb.Get(context.Background(), gameId).Result()
	if err != nil {
		return nil, status.Errorf(codes.Internal, err.Error())
	}

	game := &pb.Game{}
	err = json.Unmarshal([]byte(b), &game)
	if err != nil {
		return nil, status.Errorf(codes.Internal, err.Error())
	}
	return game, nil
}

func (c *GameController) saveGame(game *pb.Game) error {
	b, err := json.Marshal(game)
	if err != nil {
		return status.Errorf(codes.Internal, err.Error())
	}
	return c.Rdb.Set(context.Background(), game.GameId, string(b), 0).Err()
}
