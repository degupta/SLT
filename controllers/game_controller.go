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

	b, err := json.Marshal(game)
	if err != nil {
		return nil, status.Errorf(codes.Internal, err.Error())
	}

	err = c.Rdb.Set(context.Background(), game.GameId, string(b), 0).Err()
	if err != nil {
		return nil, status.Errorf(codes.Internal, err.Error())
	}

	return &pb.CreateGameResponse{Game: game}, nil
}

func (c *GameController) PlayBall(in *pb.BallEvent) (*pb.Game, error) {
	return nil, nil
}

func (c *GameController) GetGame(in *pb.GetGameRequest) (*pb.Game, error) {
	b, err := c.Rdb.Get(context.Background(), in.GameId).Result()
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
