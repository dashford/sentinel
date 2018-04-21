from twisted.internet import task


class Factory:

    @staticmethod
    def create_task(device, metric, poll):
        if metric == 'temperature':
            loop = task.LoopingCall(device.get_temperature)
            loop.start(poll)
            scheduler.add_job(get_temp, 'interval', seconds=5, args=[client, event_dispatcher])
        elif metric == 'pressure':
            loop = task.LoopingCall(device.get_pressure)
            loop.start(poll)
        elif metric == 'humidity':
            loop = task.LoopingCall(device.get_humidity)
            loop.start(poll)