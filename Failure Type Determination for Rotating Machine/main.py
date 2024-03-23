# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # import libraries
    import math
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # Load the data
    time_raw = pd.read_csv('data/data by group/3/B.csv', header=None).iloc[:, 1:]\
        .transpose().set_axis(["Value"], axis="columns").reset_index(drop=True)
    acc_fft = pd.read_csv('data/data by group/3/B_acc_fft.csv', header=None) \
        .transpose().set_axis(["Value"], axis="columns")
    velocity_fft = pd.read_csv('data/data by group/3/B_veloity_fft.csv', header=None) \
        .transpose().set_axis(["Value"], axis="columns")
    envelope = pd.read_csv('data/data by group/3/B_envelope.csv', header=None) \
        .transpose().set_axis(["Value"], axis="columns")

    # Enter other require data
    shaft_rpm = 1300
    sample_rate = 10240
    sample_length = 8192
    gear_info_is_given = False
    if gear_info_is_given:
        speed_reduction_ratio = 0.84
        number_of_teeth = 31
        gear_rpm = 5674.80
    bearing_info_is_given = True
    if bearing_info_is_given:
        bearing_attach_angle = 0  # in rad
        bearing_pitch_diameter = 0.807
        bearing_number_of_balls = 8
        bearing_ball_dia = 0.187

    # Calculate require parameters
    shaft_rotate_frequency = shaft_rpm / 60  # fa
    if gear_info_is_given:
        gear_mesh_frequency = gear_rpm / 60 * number_of_teeth
        fp = shaft_rotate_frequency * speed_reduction_ratio
    if bearing_info_is_given:
        f_in = 0.5 * shaft_rotate_frequency * (
                1 + bearing_ball_dia / bearing_pitch_diameter *
                math.cos(bearing_attach_angle)) * bearing_number_of_balls
        f_out = 0.5 * shaft_rotate_frequency * (
                1 - bearing_ball_dia / bearing_pitch_diameter *
                math.cos(bearing_attach_angle)) * bearing_number_of_balls
        f_roller = bearing_pitch_diameter / bearing_ball_dia * shaft_rotate_frequency * (
                1 - (bearing_ball_dia / bearing_pitch_diameter *
                     math.cos(bearing_attach_angle)) ** 2)

    # Preprocess the data
    time_axis = pd.DataFrame(np.arange(start=0, stop=sample_length, step=1) / sample_rate, columns=['time'])
    time_raw = pd.concat([time_raw, time_axis], axis=1)
    frequency_resolution = sample_rate / sample_length
    frequency_axis = pd.DataFrame(np.arange(start=0, stop=sample_length / 2, step=1) * frequency_resolution,
                                  columns=['frequency'])
    acc_fft = pd.concat([acc_fft, frequency_axis], axis=1)
    velocity_fft = pd.concat([velocity_fft, frequency_axis], axis=1)
    envelope = pd.concat([envelope, frequency_axis], axis=1)

    # Plot the data
    fig, ax = plt.subplots(4)
    ax[0].plot('time', 'Value', data=time_raw)
    ax[0].set_title('Time Data')
    ax[1].plot('frequency', 'Value', data=acc_fft)
    ax[1].set_title('Acceleration FFT Data')
    ax[2].plot('frequency', 'Value', data=velocity_fft)
    ax[2].set_title('Velocity FFT Data')
    ax[3].plot('frequency', 'Value', data=envelope)
    ax[3].set_title('Envelope Diagram')
    plt.sca(ax[0])
    plt.xticks(np.arange(time_raw['time'].min(), time_raw['time'].max(), 0.05))
    ax[0].set(xlabel='Time (s)')
    plt.sca(ax[1])
    plt.xticks(np.arange(acc_fft['frequency'].min(), acc_fft['frequency'].max(), 50))
    ax[1].set(xlabel='Frequency (Hz)')
    plt.sca(ax[2])
    plt.xticks(np.arange(velocity_fft['frequency'].min(), velocity_fft['frequency'].max(), 50))
    ax[2].set(xlabel='Frequency (Hz)')
    plt.sca(ax[3])
    plt.xticks(np.arange(envelope['frequency'].min(), envelope['frequency'].max(), 50))
    ax[3].set(xlabel='Frequency (Hz)')
    plt.subplots_adjust(hspace=0.8)
    plt.show()

