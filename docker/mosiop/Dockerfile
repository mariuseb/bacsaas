FROM buildopt:core

ENV DEBIAN_FRONTEND=noninteractive

# UID and GID as obtained from bacssaas user on ROME id -u, id -g
ARG USER_NAME
#
# generic packages
#

#RUN useradd -d /home/${USER_NAME} -m ${USER_NAME} && \
#     chown -R ${USER_NAME} /home/${USER_NAME} && \
#     adduser ${USER_NAME} sudo && \
#     echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN sudo apt-get update && sudo apt-get install -y \
         python3-pyqt5 \
         curl \
         pip \
         dvipng \
         texlive-latex-extra \
         texlive-fonts-recommended \
         cm-super \
         r-base \
         nvidia-cuda-toolkit

#RUN 73 | sudo apt-get install keyboard-configuration


# install python depencies
ADD /include ./mosiop

###### fetch and install intel mkl ########

#RUN wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB
#RUN apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB


## all products:
#sudo wget https://apt.repos.intel.com/setup/intelproducts.list -O /etc/apt/sources.list.d/intelproducts.list
## just MKL
#RUN sh -c 'echo deb https://apt.repos.intel.com/mkl all main > /etc/apt/sources.list.d/intel-mkl.list'
## other (TBB, DAAL, MPI, ...) listed on page

#RUN apt-get update
#RUN apt-get install -y intel-mkl-64bit-2018.2-046   ## wants 500+mb :-/  installs to 1.8 gb :-/

## update alternatives
#RUN update-alternatives --install /usr/lib/x86_64-linux-gnu/libblas.so     libblas.so-x86_64-linux-gnu      /opt/intel/mkl/lib/intel64/libmkl_rt.so 150
#RUN update-alternatives --install /usr/lib/x86_64-linux-gnu/libblas.so.3   libblas.so.3-x86_64-linux-gnu    /opt/intel/mkl/lib/intel64/libmkl_rt.so 150
#RUN update-alternatives --install /usr/lib/x86_64-linux-gnu/liblapack.so   liblapack.so-x86_64-linux-gnu    /opt/intel/mkl/lib/intel64/libmkl_rt.so 150
#RUN update-alternatives --install /usr/lib/x86_64-linux-gnu/liblapack.so.3 liblapack.so.3-x86_64-linux-gnu  /opt/intel/mkl/lib/intel64/libmkl_rt.so 150

#RUN echo "/opt/intel/lib/intel64"     >  /etc/ld.so.conf.d/mkl.conf
#RUN echo "/opt/intel/mkl/lib/intel64" >> /etc/ld.so.conf.d/mkl.conf
#RUN ldconfig

#RUN echo "MKL_THREADING_LAYER=GNU" >> /etc/environment

#################################################
    
#RUN pip install --upgrade pip --no-cache-dir -r ./mosiop/requirements.txt
#RUN which python
RUN sudo pip install --no-cache-dir -r ./mosiop/requirements.txt
# additional packages, a.t. cpu versions of torch:
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
#

# for learning etc.:
#RUN pip install l4casadi --no-build-isolation
#RUN pip install --no-cache-dir torchvision --index-url https://download.pytorch.org/whl/cpu
#RUN pip3 install -e /opt/acados/interfaces/acados_template

RUN sudo apt-get update
RUN sudo apt-get install ca-certificates curl gnupg sudo
RUN curl -fsSL http://build.openmodelica.org/apt/openmodelica.asc | \
  sudo gpg --dearmor -o /usr/share/keyrings/openmodelica-keyring.gpg

RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/openmodelica-keyring.gpg] \
  https://build.openmodelica.org/apt \
  jammy \
  release" | sudo tee /etc/apt/sources.list.d/openmodelica.list

RUN sudo apt update
RUN sudo apt install -y openmodelica

# delete scs from cvxpy
#RUN sudo rm -rf /usr/local/lib/python3.10/site-packages/scs && \
#    sudo rm -rf /usr/local/lib/python3.10/site-packages/scs-3.2.2.dist-info && \
#    sudo rm -rf /usr/local/lib/python3.10/site-packages/scs.libs

# re-build SCS with openmp and mkl (https://groups.google.com/g/cvxpy/c/qyiA94ojb_A)
#WORKDIR /opt
#RUN sudo git clone --recursive https://github.com/bodono/scs-python.git \
#    && cd scs-python \
#    && sudo python setup.py install --scs --openmp

#RUN useradd -d /home/${USER_NAME} -m ${USER_NAME} && \
#     chown -R ${USER_NAME} /home/${USER_NAME} && \
#     adduser ${USER_NAME} sudo && \
#     echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# to watch omp:
RUN sudo apt-get install htop
# now, after building scs, install cvxpy:
RUN sudo pip install --no-cache-dir cvxpy-base

USER $USER_NAME
ENV HOME /home/$USER_NAME
ARG workdir=/home/$USER_NAME
WORKDIR $workdir

# copy mosek.lic to lib path:
#RUN mkdir /home/$USER_NAME/mosek
#ADD /include/mosek.lic /home/$USER_NAME/mosek/mosek.lic
#
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"
ENV OMP_NUM_THREADS=1
ENV USER=om

RUN echo -e '\n \e[1;34mInstallation complete\033[0m \n'


