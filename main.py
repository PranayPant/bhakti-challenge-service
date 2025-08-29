            "elapsed_seconds": elapsed,
            "time_taken": time_taken
        })
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()
