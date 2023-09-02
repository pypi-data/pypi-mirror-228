from distutils.core import setup
setup(
  name = 'cvworld',         # How you named your package folder (MyLib)
  packages = ['cvworld'],   # Chose the same as "name"
  version = '1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Computer Vision Helper Function',   # Give a short description about your library
  author = 'Sethu Raman',                   # Type in your name
  author_email = 'sethuramanvr046@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/sethuraman17/Game_Automation',   # Provide either the link to your github or to your website
  linkedin = 'https://www.linkedin.com/in/sethu-raman-931a62211',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['ComputerVision', 'FaceDetection', 'HandTracking'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'opencv-python',
          'mediapipe',
          'cvzone'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)