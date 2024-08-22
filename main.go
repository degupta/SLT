package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"
	"slt/controllers"
	"slt/pb"

	redis "github.com/redis/go-redis/v9"
	"google.golang.org/grpc"
)

type server struct {
	pb.UnimplementedGameServiceServer
	controller *controllers.GameController
}

func (s *server) CreateGame(ctx context.Context, in *pb.CreateGameRequest) (*pb.CreateGameResponse, error) {
	return s.controller.CreateGame(in)
}

func (s *server) PlayBall(ctx context.Context, in *pb.PlayBallRequest) (*pb.Game, error) {
	return s.controller.PlayBall(in)
}

func (s *server) GetGame(ctx context.Context, in *pb.GetGameRequest) (*pb.Game, error) {
	return s.controller.GetGame(in)
}

func main() {
	flag.Parse()
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", 5051))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password set
		DB:       0,  // use default DB
	})

	controller := &controllers.GameController{Rdb: rdb}

	s := grpc.NewServer()
	pb.RegisterGameServiceServer(s, &server{controller: controller})
	log.Printf("server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
